from openpyxl import load_workbook
from config import markets


class EpConverter:
    def __init__(self):
        self.workbook = load_workbook('src/udlinitel.xlsx')
        self.products = {}

    def run(self):
        self.load_products()
        self.data_out()

    def load_products(self):
        for row in self.workbook.active:
            if not row[0].value:
                continue
            platform = self.get_platform(row[0].value)
            rosel_id = row[2].value
            name = row[3].value
            commodity = row[1].value
            if not self.products.get(rosel_id):
                self.products[rosel_id] = {'name': name, 'commodity': commodity, 'competitors': {}}
            merch = self.products[rosel_id]
            url = row[4].value
            if merch['competitors'].get(platform):
                merch['competitors'][platform].append(url)
            else:
                merch['competitors'][platform] = [url]

    def get_platform(self, shop_url):
        platforms = list(markets)
        for shop in platforms:
            if shop in shop_url:
                return shop

    def data_out(self):
        print(self.products)


if __name__ == '__main__':
    conv = EpConverter()
    conv.run()
