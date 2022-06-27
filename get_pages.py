import datetime
import time
from random import randint
from threading import Thread
import requests
from config import req_headers, selenium_arguments, browser_path
from utilites import check_dir
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class PageGetter(Thread):
    def __init__(self, platform, links):
        super().__init__()
        self.platform = platform
        self.links = links
        self.date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.use_selenium = False
        self.check_for_using_selenium()
        self.cur_html_data = None
        self.browser = None
        self.filename = None

    def check_for_using_selenium(self):
        match self.platform in ['baucenter']:
            case True:
                self.use_selenium = True
            case _:
                self.use_selenium = False

    def run(self):
        check_dir(f'htmls/{self.date}/{self.platform}_files/')
        if self.use_selenium:
            self.initiate_browser()
        self.get_pages()
        if self.browser:
            self.browser.close()

    def initiate_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument(selenium_arguments[0])
        options.add_argument(selenium_arguments[1])
        self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)

    def get_pages(self):
        ll = len(self.links)
        for order, url in enumerate(self.links, start=1):
            wait_time = randint(5, 15)
            print(f'{self.platform:>10} ({order:03} / {ll:03}), waiting: {wait_time:3} | connecting to url: {url}')
            self.get_page(url)
            time.sleep(wait_time)
            self.filename = url.split('/')[-2]
            self.save_page()

    def get_page(self, url):
        if self.use_selenium:
            self.browser.get(url=url)
            self.scroll_down()
            self.cur_html_data = self.browser.page_source
        else:
            try:
                req = requests.get(url, headers=req_headers)
                self.cur_html_data = req.text
            except requests.exceptions.SSLError as ex:
                print(f'ERROR: {ex}, URL: {url}')

    def save_page(self):
        filename = f'htmls/{self.date}/{self.platform}_files/{self.filename}.html'
        with open(filename, 'w', encoding='utf8') as write_file:
            write_file.write(self.cur_html_data)

    def scroll_down(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(1)
        while True:
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            if new_height == last_height:
                break
            last_height = new_height
