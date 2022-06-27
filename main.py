from get_pages import PageGetter
from utilites import get_product_links, time_track


@time_track
def get_pages():
    platform_links = get_product_links()
    getters = [PageGetter(platform, goods) for platform, goods in platform_links.items()]
    for getter in getters:
        getter.start()
    for getter in getters:
        getter.join()


@time_track
def parse_pages():
    pass


if __name__ == '__main__':
    get_pages()
    parse_pages()
