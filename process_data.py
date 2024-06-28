import os
import pandas as pd
from document import DocumentPdf
from identify_data import BuildData
from transform import TransformPdf


class ProcessData:

    def __init__(self, directory):
        self.dir = directory
        self.file_paths = []

        id_data = BuildData()
        id_data.find_dl_meta_data()
        id_data.find_meta_data_values()

        self.dl_dict = id_data.dl_dict
        self.opp_list = id_data.data_list

        self.df_list = []

    def run(self):
        self.walk_files()
        for fp in self.file_paths:
            print(fp)
            base, ext = self.get_base_and_ext(fp)
            title, publish = self.get_opportunity_data(base)

            if ext == ".pdf":
                doc = DocumentPdf(file_path=fp)
                doc.read_text()
                text = TransformPdf(document=doc)
                text.transform()

            df_dict = {"Opportunity": [title] * len(text.data),
                       "PublishDate": [publish] * len(text.data),
                       "Text": text.data}
            tmp_df = pd.DataFrame(df_dict)
            self.df_list.append(tmp_df)
            break
        

    def walk_files(self):
        for dirpath, _, filenames in os.walk(self.dir):
            for f in filenames:
                if not f.startswith("."):
                    self.file_paths.append(os.path.abspath(os.path.join(dirpath, f)))

    def get_base_and_ext(self, filename):
        base = os.path.basename(filename)
        _, ext = os.path.splitext(base)
        base = self._correct_basename(base)
        return base, ext

    def _correct_basename(self, base):
        base = base.replace("+", " ")
        base = base.replace("%28", "(")
        base = base.replace("%29", ")")
        return base

    def get_opportunity_id(self, filename):
        for opp, val in self.dl_dict.items():
            for v in val:
                if filename in v.values():
                    return opp
                
    def get_opportunity_data(self, filename):
        f = self.get_opportunity_id(filename=filename)
        opp = list(filter(lambda _title: _title['_id'] == f, self.opp_list))[0]
        title = opp['title']
        publish_date = opp['publishDate']
        return title, publish_date


if __name__ in "__main__":
    DIR = "./download_data/"
    p = ProcessData(DIR)
    p.run()
    # base, ext = p.get_base_and_ext(FILE)
    # opp_id = p.get_opportunity_data(base)