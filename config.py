import sys

match sys.platform:
    case 'linux':
        browser_path = None
        user_agent = None
    case 'darwin':
        browser_path = 'drivers/chromedriver'
        user_agent = None
    case 'win32':
        browser_path = 'drivers/chromedriver.exe'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    case _:
        print("ERROR: can't found selenium driver")
        user_agent = None

markets = {
    'maxidom': 'https://www.maxidom.ru/',
    'leroy': 'https://spb.leroymerlin.ru/',
    'megastroy': 'https://megastroy.com/',
    'baucenter': 'https://baucenter.ru/',
    'dns': 'https://www.dns-shop.ru/',
    'petrovich': 'https://petrovich.ru/',
    'vprok': 'https://www.vprok.ru/',
    'ststroitel': 'https://www.ststroitel.ru/'
}

selenium_arguments = [f'user-agent={user_agent}', '--disable-blink-features=AutomationControlled']
req_headers = {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'user-agent': user_agent}
