import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook

from config import req_headers
from utilites import get_platform


def get_page(url):
    try:
        req = requests.get(url, headers=req_headers)
        return BeautifulSoup(req.text, 'lxml')
    except requests.exceptions.SSLError as ex:
        print(f'ERROR: {ex}, URL: {url}')
        return None


class EpConverter:
    def __init__(self):
        self.workbook = load_workbook('src/price_monitoring.xlsx')
        self.products = {}
        self.platform = None
        self.parser = None
        self.no_rosel_id = 0

    def run(self):
        self.load_products()
        self.data_out()

    def load_products(self):
        sw = self.workbook.active
        for row in sw:
            if not row[0].value:
                continue
            platform = get_platform(row[0].value)
            if not platform:
                continue
            commodity = row[1].value
            if commodity == 'Детское ТН':  # Детское ТН не мониторим
                continue
            self.platform = platform
            rosel_id = row[2].value
            if not rosel_id:
                self.no_rosel_id += 1
                rosel_id = f'noid{self.no_rosel_id:3}'
            else:
                rosel_id = self.convert_id(rosel_id)
            shop_id = self.convert_id(row[3].value)
            search_url = self.set_search_url(shop_id)
            name = row[4].value
            products = self.products
            if not products.get(rosel_id):
                products[rosel_id] = {'name': name, 'commodity': commodity, 'competitors': {}}
            merch = products[rosel_id]
            # self.get_data_from_search(search_id)
            if merch['competitors'].get(platform):
                merch['competitors'][platform].append(search_url)
            else:
                merch['competitors'][platform] = [search_url]

    def data_out(self):
        print(self.products)

    def set_search_url(self, art):
        match self.platform:
            case 'baucenter':
                url = f'https://baucenter.ru/search/?q={art}'
            case 'leroy':
                url = f'https://spb.leroymerlin.ru/search/?q={art}'
            case 'maxidom':
                url = f'https://www.maxidom.ru/search/catalog/?q={art}'
            case 'dns':
                url = f'https://www.dns-shop.ru/search/?q={art}'
            case 'megastroy':
                url = f'https://kazan.megastroy.com/catalog/search?q={art}'
            case 'vprok':
                url = f'https://www.vprok.ru/catalog/search?text={art}'
            case _:
                url = None
        return url

    def convert_id(self, art):
        shop_id_divided = str(art).split('\u200c')
        return int(''.join(shop_id_divided))


if __name__ == '__main__':
    conv = EpConverter()
    conv.run()
