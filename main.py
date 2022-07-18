import os

from config import markets
from data_getter import DataGetter
from get_pages import PageGetter
from utilites import divide_goods_by_platforms, time_track, get_last_dir


@time_track
def get_pages():
    platform_links = divide_goods_by_platforms()
    getters = [PageGetter(platform, goods) for platform, goods in platform_links.items()]
    for getter in getters:
        getter.start()
    for getter in getters:
        getter.join()


@time_track
def parse_pages():
    last_htmls_folder = f'htmls/{get_last_dir()}'
    platforms_folders = [f'{last_htmls_folder}/{folder}' for folder in os.listdir(last_htmls_folder)]
    for folder in platforms_folders:
        DataGetter(folder).run()


if __name__ == '__main__':
    # get_pages()
    parse_pages()
