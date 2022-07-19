import os
from data_getter import DataGetter
from get_pages import PageGetter
from make_result_xlsx_from_jsons import JsonToXlsConverter
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
    last_folder = f'web_loads/{get_last_dir()}'
    platforms_folders = [f'{last_folder}/{folder}' for folder in os.listdir(last_folder)]
    for folder in platforms_folders:
        DataGetter(folder).run()


@time_track
def create_result_xls_from_json():
    last_folder = 'json_from_web_loads/' + get_last_dir('json_from_web_loads')
    res = JsonToXlsConverter(last_folder)
    res.run()


if __name__ == '__main__':
    # get_pages()
    # parse_pages()
    create_result_xls_from_json()
