from datetime import datetime
import os
import re
import time

from config import markets
from src.goods import goods


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        minutes = round(elapsed / 60, 4)
        print(f'\nФункция работала {elapsed} секунд(ы), или {minutes} минут')
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


def get_product_links():
    all_goods_in_platforms = {}
    used_platforms = list(markets.keys())
    for rosel_id in goods:
        merch = goods[rosel_id]
        current_platforms = merch['competitors']
        for platform in current_platforms:
            if not platform in used_platforms:
                continue
            shop_goods = current_platforms[platform]
            if not all_goods_in_platforms.get(platform):
                all_goods_in_platforms[platform] = []
            all_goods_in_platforms[platform].extend(shop_goods)
    return all_goods_in_platforms
