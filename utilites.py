from datetime import datetime
import os
import re
import time
from config import markets
from src.stock_from_xls import stock


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        minutes = round(elapsed / 60, 4)
        print(f'\nФункция работала {elapsed} секунд(ы), или {minutes:2} минут')
        return result

    return surrogate


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_last_dir(directory='htmls'):
    dir_template, date_template = r'202\d-\d{2}-\d{2}', '%Y-%m-%d'
    dates_dirs = [datetime.strptime(el, date_template) for el in os.listdir(directory) if re.findall(dir_template, el)]
    final_dir = sorted(dates_dirs)[-1].strftime(date_template)
    return final_dir


def divide_goods_by_platforms():
    pl = {}
    used_platforms = list(markets.keys())
    for rosel_id in stock:
        platform_competitors = stock[rosel_id]['competitors']
        for shop, shop_goods in platform_competitors.items():
            if not shop in used_platforms:
                continue
            if not pl.get(shop):
                pl[shop] = []
            pl[shop].extend(shop_goods)
    return pl


def get_platform(shop_url):
    platforms = list(markets)
    for shop in platforms:
        if shop in shop_url:
            return shop
    return None
