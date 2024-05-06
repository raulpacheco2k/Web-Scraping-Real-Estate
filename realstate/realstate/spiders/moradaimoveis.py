import re

import scrapy
import unicodedata
from scrapy_splash import SplashRequest


class Sanitize:
    @staticmethod
    def clean(text):
        text = unicodedata.normalize('NFKD', text)
        text = re.sub('[^A-Za-z0-9_ ,.]+', '', text)
        text = text.replace('  ', ' ')
        text = text.strip()

        return text


class MoradaImoveis(scrapy.Spider):
    name = 'Morada Imoveis'
    allowed_domains = ['moradaimoveistb.com.br']
    start_urls = [
        'https://moradaimoveistb.com.br/alugar/imoveis?sort=-is_price_shown%2C-calculated_price%2Cid&offset=1&limit=21&typeArea=total_area&floorComparision=equals']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)

    def parse(self, response, **kwargs):
        print(len(response.css('.CardProperty')))
        print(len(response.css('.CardProperty')))
        print(len(response.css('.CardProperty')))
        print(len(response.css('.CardProperty')))
        print(len(response.css('.CardProperty')))
