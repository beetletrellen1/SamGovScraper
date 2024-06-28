import requests
import json
import time
import random
import wget

from identify_data import BuildData


class CaptureSamWebsite:

    def __init__(self):
        self.url = None
        self.counter = 0
    
        self.req = None
        self.response_ok = True
        self.data_list = []
    
        self.filename = None
    
    def update_URL(self):
        pass

    def run(self):
        print("Initializing Website Search")
        self.update_URL()
        while self.response_ok:
            if self.counter % 100 == 0:
                print(self.counter)

            self.GET()
            self.capture_data()
            
            self.counter += 1
            self.update_URL()

        self.write_json_data()
    
    def GET(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        self.req = requests.get(self.url, headers = headers)
        self.check_response()

    def check_response(self):
        self.response_ok = self.req.ok
        if not self.response_ok:
            print("Scrape Ended on:", self.counter)

    def capture_data(self):
        txt = self.req.text
        data = json.loads(txt)
        self.data_list.append(data)

    def write_json_data(self):
        print(f"Creating {self.filename}")
        json_object = json.dumps(self.data_list, indent=4)
        with open(self.filename, "w") as outfile:
            outfile.write(json_object)


class CaptureSamWebsiteMetaData(CaptureSamWebsite):

    def __init__(self):
        super().__init__()
        self.filename = "meta_data.json"

    def update_URL(self):
        rand_number = random.randint(100000000, 3685299157419)
        self.url = f"https://sam.gov/api/prod/sgs/v1/search/?random={rand_number}&index=opp&page={self.counter}&sort=-modifiedDate&size=25&mode=search&responseType=json&is_active=true"


class CaptureSamWebsiteMainPage(CaptureSamWebsite):
    
    def __init__(self):
        super().__init__()

        id_data = BuildData()
        id_data.find_meta_data_values()
        id_data.create_list_ID()
        self.id_list = id_data.meta_id

        self.filename = "full_page_data.json"

    def update_URL(self):
        rand_number = random.randint(100000000, 3685299157419)
        page_id = self.id_list[self.counter]
        self.url = f"https://sam.gov/api/prod/opps/v2/opportunities/{page_id}?random={rand_number}"
        if self.counter == (len(self.id_list)-1):
            self.response_ok = False


class CaptureSamWebsiteDownloadMetaData(CaptureSamWebsite):

    def __init__(self):
        super().__init__()

        id_data = BuildData()
        id_data.find_meta_data_values()
        id_data.create_list_ID()
        self.id_list = id_data.meta_id

        self.filename = "dl_meta_data.json"

    def update_URL(self):
        rand_number = random.randint(100000000, 3685299157419)
        page_id = self.id_list[self.counter]
        self.url = f"https://sam.gov/api/prod/opps/v3/opportunities/{page_id}/resources?random={rand_number}&excludeDeleted=false&withScanResult=false"
        if self.counter == (len(self.id_list)-1):
            self.response_ok = False

class CaptureSamWebsiteDownloadAttach(CaptureSamWebsite):

    def __init__(self):
        super().__init__()
        
        id_data = BuildData()
        id_data.find_dl_meta_data()
        id_data.create_list_resource_ID()
        self.resource_id = id_data.resource_id_list

        self.missed_dl = 0
        self.counter = 1

    def run(self):
        print("Initializing Downloads Search")
        self.update_URL()
        while self.response_ok:
            percent_complete = self.counter / len(self.resource_id) * 100
            if percent_complete % 20 == 0:
                print(f"Download is {percent_complete}% complete")
            self.GET()
            
            self.counter += 1
            self.update_URL()
        print(f"Attempted to Download {self.counter} files")
        print(f"Total Files Actually Downloaded: {self.missed_dl}")

    def update_URL(self):
        resource_id = self.resource_id[self.counter]-1
        self.url = f"https://sam.gov/api/prod/opps/v3/opportunities/resources/files/{resource_id}/download?&token="
        print(self.url)

    def GET(self):
        try:
            wget.download(self.url, out = "./download_data")
        except:
            print("Unable to Download File:", self.url)
            self.missed_dl += 1


if __name__ in "__main__":
    # ws = CaptureSamWebsiteMetaData()
    # ws = CaptureSamWebsiteMainPage()
    # ws = CaptureSamWebsiteDownloadMetaData()
    ws = CaptureSamWebsiteDownloadAttach()
    ws.run()