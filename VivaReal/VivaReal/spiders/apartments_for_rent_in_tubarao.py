import re
from unidecode import unidecode

import scrapy
import unicodedata


def sanitize(text):
    text = unicodedata.normalize('NFKD', text)
    text = re.sub('[^A-Za-z0-9_ ]+', '', text)
    text = text.replace('  ', ' ')
    text = text.strip()

    return text


class ApartmentsForRentInTubarao(scrapy.Spider):
    name = 'VivaReal'
    start_urls = ['https://www.vivareal.com.br/aluguel/santa-catarina/tubarao/apartamento_residencial/']

    def parse(self, response, **kwargs):
        for apartments in response.css('a.js-card-title'):
            yield {
                'title': sanitize(apartments.css('div h2 span::text')[0].get()),
                'price': sanitize(apartments.css('div section div p::text').get()).replace('R ', ''),
                'period': sanitize(apartments.css('div section div p span::text').get()).replace('/', ''),
                'address': sanitize(apartments.css('div h2 span')[1].css('span::text')[1].get()),
                'squareMeter': sanitize(apartments.css('div ul')[0].css('li')[0].css('span::text')[0].get()),
                'bedrooms': sanitize(apartments.css('div ul')[0].css('li')[1].css('span::text')[0].get()),
                'bathroom': sanitize(apartments.css('div ul')[0].css('li')[2].css('span::text')[0].get()),
                'parkingSpaces': sanitize(apartments.css('div ul')[0].css('li')[3].css('span::text')[0].get())
            }
