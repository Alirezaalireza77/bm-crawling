import scrapy
import time
import tempfile
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class CarSpider(scrapy.Spider):
    name = 'bama'
    allowed_domains = ['bama.ir']
    start_urls = [
        'https://www.bama.ir/car?page=1',
    ]

    def __init__(self, *args, **kwargs):
        super(CarSpider, self).__init__(*args, **kwargs)
        options = Options()
        options.headless = True

        options.add_argument('--no-sandbox')  # Required for running as root
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource issues
        options.add_argument('--disable-gpu')  # Disable GPU for headless mode
        options.add_argument('--remote-debugging-port=9222')  # Enable remote debugging

        profile_dir = tempfile.mkdtemp()
        options.add_argument(f"user-data-dir={profile_dir}")

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def parse(self, response):
        self.driver.get(response.url)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        sel = Selector(text=self.driver.page_source)
        car_links = sel.xpath('//div[@class="bama-adlist-container"]//a/@href').extract()

        for link in car_links:
            yield response.follow(link, callback=self.parse_car)

        self.driver.quit()

    def parse_car(self, response):
        # Extract car model and price
        model = response.xpath('normalize-space(//h1[@class="bama-ad-detail-title__title"])').get()
        price = response.xpath(
            'normalize-space(//div[@class="bama-ad-detail-price__section"]//span[@class="bama-ad-detail-price__price-text"])').get()

        yield {
            'model': model,
            'price': price if price else None
        }
