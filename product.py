from config import markets


class Product:
    def __init__(self):
        self.rosel_id = None
        self.name = None
        self.commodity = None
        self.rosel_price = None
        self.mp = {}
        self.set_shops()

    def set_shops(self):
        for shop in markets:
            self.mp[shop] = Shop(shop)
            self.mp[shop].shop_url = markets[shop]

    def data_out(self):
        return {self.rosel_id}


class Shop:
    def __init__(self, name):
        self.name = name
        self.shop_url = None
        self.prod_url = None
        self.price = None
        self.price_without_discount = None
        self.competitors = {}


class Competitor:
    def __init__(self):
        self.platform = None
        self.rosel_id = None
        self.commodity = None
        self.competitor_url = None
