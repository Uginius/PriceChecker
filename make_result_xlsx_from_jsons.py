import json
import os
from openpyxl import load_workbook
from utilites import get_platform, check_dir


class JsonToXlsConverter:
    def __init__(self, folder):
        self.src_folder = folder
        self.json_files = os.listdir(folder)
        self.date = folder.split('/')[1]
        self.platform_prices = {}
        self.workbook = load_workbook('src/price_monitoring.xlsx')

    def run(self):
        self.load_data()
        self.workbook.active.insert_cols(5, amount=1)
        self.extend_table()
        self.write_result()

    def load_data(self):
        for json_filename in self.json_files:
            platform = json_filename.split('.')[0]
            with open(f'{self.src_folder}/{json_filename}', 'r', encoding='utf8') as read_file:
                data = json.load(read_file)
            self.platform_prices[platform] = data

    def extend_table(self):
        sw = self.workbook.active
        for line in sw:
            platform = get_platform(line[0].value)
            if not platform:
                continue
            search_id = str(line[3].value)
            price = self.platform_prices[platform].get(search_id)
            line[4].value = price

    def write_result(self):
        check_dir('xls_results')
        self.workbook.save(f"xls_results/{self.date}.xlsx")


