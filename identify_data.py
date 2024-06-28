import json


class BuildData:
    def __init__(self):
        self.data_list = []
        self.meta_id = []

        self.meta_data_file = "meta_data.json"
        self.meta_data_keys = ['isCanceled', '_type', 'publishDate', 'isActive', 'title', '_id']

        self.dl_dict = {}
        self.meta_dl_file = "dl_meta_data.json"
        self.meta_dl_keys = ['resourceId', 'name', 'type', 'postedDate']

        self.resource_id_list = []

    def find_meta_data_values(self):
        with open(self.meta_data_file, "r") as f:
            j = json.load(f)
            for idx in range(len(j)-1):
                for i in range(0,25):
                    data_dict = {}
                    for key in self.meta_data_keys:
                        data_dict[key] = j[idx]["_embedded"]['results'][i][key]
                    self.data_list.append(data_dict)

            print("Number of Records:", len(self.data_list))
            print("Number of Keys per Record:", len(self.data_list[0]))

    def create_list_ID(self):
        data = self.data_list
        self.meta_id = list(map(lambda id: id['_id'], data))
        print("Unique ID Count:", len(set(self.meta_id)))

    def find_dl_meta_data(self):
        data_dict = {}
        with open(self.meta_dl_file, "r") as f:
            j = json.load(f)
            for idx in range(len(j)):
                for i in range(len(j[0]['_embedded']['opportunityAttachmentList'])):
                    self.meta_dl_list = []
                    try:
                        opp = j[idx]['_embedded']['opportunityAttachmentList'][i]
                        op_id = opp['opportunityId']
                        data_list = []
                        for attachment in range(len(opp['attachments'])):
                            data_dict = {}
                            for key in self.meta_dl_keys:
                                data_dict[key] = opp['attachments'][attachment][key]
                            data_list.append(data_dict)
                        self.dl_dict[op_id] = data_list
                    except KeyError as e:
                        pass
                        # print(f"Index does not have {e}")
            print("Number of Records:", len(self.dl_dict))

    def create_list_resource_ID(self):
        for k in self.dl_dict.keys():
            for i in range(len(self.dl_dict[k])):
                if self.dl_dict[k][i]['type'] == 'file':
                    self.resource_id_list.append(self.dl_dict[k][i]['resourceId'])
        print("files_to_download:", len(self.resource_id_list))

if __name__ in "__main__":
    id_data = BuildData()
    id_data.find_dl_meta_data()
    # print(id_data.dl_dict)
    # id_data.create_list_resource_ID()
    id_data.find_meta_data_values()
    print(id_data.data_list)
    # id_data.create_list_ID()