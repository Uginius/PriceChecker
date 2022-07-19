import json
import os
from bs4 import BeautifulSoup
from utilites import get_platform, check_dir


class DataGetter:
    def __init__(self, folder):
        self.folder = folder
        self.date = folder.split('/')[1]
        self.platform = get_platform(folder)
        self.merch_id = None
        self.files = sorted(os.listdir(folder))
        self.soup = None
        self.goods = {}

    def run(self):
        print(self.platform)
        # if self.platform in ['baucenter', 'dns', 'maxidom', 'megastroy']:
        #     return
        for filename in self.files:
            self.merch_id = filename.split('.')[0]
            with open(f'{self.folder}/{filename}', 'r', encoding='utf8') as read_file:
                if read_file == '.DS_Store':
                    continue
                src = read_file.read()
            self.soup = BeautifulSoup(src, 'lxml')
            self.get_data()
        self.write_json()

    def get_data(self):
        self.get_price()

    def get_price(self):
        match self.platform:
            case 'baucenter':
                scripts = self.soup.find_all('script', attrs={})
                dirty_json = None
                for order, scr in enumerate(scripts):
                    text = scr.text
                    if 'curJson' in text:
                        dirty_json = text.strip().split('curJson = ')[1].split(';\n')[0]
                        break
                if dirty_json:
                    data = json.loads(dirty_json)['ecommerce']
                    self.goods[self.merch_id] = float(data['tagparams']['totalValue'])
                else:
                    self.goods[self.merch_id] = None

            case 'dns':
                if self.soup.find('div', class_='low-relevancy'):
                    price = None
                else:
                    price_block = self.soup.find('div', class_='product-buy__price')
                    price = float(price_block.text.split('₽')[0].replace(' ', '')) if price_block else None
                self.goods[self.merch_id] = price

            case 'maxidom':
                no_found_list = list(self.soup.find_all('h3'))
                if no_found_list:
                    for el in no_found_list:
                        if 'К сожалению, по Вашему запросу ничего не найдено' in el.text:
                            self.goods[self.merch_id] = 'по Вашему запросу ничего не найдено'
                            return
                goods_list = self.soup.find('section', class_='items-list').find_all('article')
                if len(goods_list) == 1:
                    price_block = goods_list[0].find('span', class_='price-list')
                    price = float(price_block.span['data-repid_price'])
                else:
                    price = 'Неоднозначная идентификация'
                self.goods[self.merch_id] = price

            case 'megastroy':
                price = float(self.soup.find('div', class_='price').b.text.replace(' ', ''))
                self.goods[self.merch_id] = price

            case 'vprok':
                no_found = self.soup.find('div', class_='xf-empty-search__message')
                if no_found:
                    self.goods[self.merch_id] = 'по Вашему запросу ничего не найдено'
                    return
                price = float(self.soup.find('title').text.split('по цене ')[1].split(' руб.')[0])
                self.goods[self.merch_id] = price

            case _:
                pass

    def write_json(self):
        folder = f'json_from_web_loads/{self.date}'
        check_dir(folder)
        with open(f'{folder}/{self.platform}.json', 'w', encoding='utf8') as fp:
            json.dump(self.goods, fp, ensure_ascii=False)
