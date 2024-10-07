import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CarSpider(CrawlSpider):
    name = 'bama'
    allowed_domains = ['bama.ir']
    start_urls = ['https://www.bama.ir/car']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="bama-adlist-container"]//a'), callback='parse_pricing',
             follow=False),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="bama-ad listing"]/href'), follow=True),
    )

    def parse_pricing(self, response):

        model = response.xpath('normalize-space(//h1[@class="bama-ad-detail-title__title"])').get()
        price = response.xpath('normalize-space(//div[@class="bama-ad-detail-price__section"]//span[@class="bama-ad-detail-price__price-text"])').get()

        yield {
            'model': model,
            'price': price if price else None
        }



#
# import scrapy
# from scrapy.selector import Selector
# from scrapy.crawler import CrawlerProcess
# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
# import tempfile
#
# class CarSpider(scrapy.Spider):
#     name = 'bama'
#     allowed_domains = ['bama.ir']
#     start_urls = ['https://www.bama.ir/car']
#
#     def __init__(self, *args, **kwargs):
#         super(CarSpider, self).__init__(*args, **kwargs)
#         options = webdriver.FirefoxOptions()
#         options.headless = True  # Run in headless mode
#
#         profile_dir = tempfile.mkdtemp()
#         options.profile = profile_dir
#
#         self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
#
#     def parse(self, response):
#         self.driver.get(response.url)
#
#         last_height = self.driver.execute_script("return document.body.scrollHeight")
#         while True:
#             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)
#
#             new_height = self.driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height
#
#         sel = Selector(text=self.driver.page_source)
#         car_links = sel.xpath('//div[@class="bama-adlist-container"]//a/@href').extract()
#
#         for link in car_links:
#             yield response.follow(link, callback=self.parse_car)
#
#         self.driver.quit()
#
#     def parse_car(self, response):
#         model = response.xpath('normalize-space(//h1[@class="bama-ad-detail-title__title"])').get()
#         price = response.xpath('normalize-space(//div[@class="bama-ad-detail-price__section"]//span[@class="bama-ad-detail-price__price-text"])').get()
#
#         yield {
#             'model': model,
#             'price': price if price else None
#         }
