import re
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
        apartments = response.css('a.js-card-title')
        for apartment in apartments:
            yield {
                'title': sanitize(apartment.css('div h2 span::text')[0].get()),
                'price': sanitize(apartment.css('div section div p::text').get()).replace('R ', ''),
                'period': sanitize(apartment.css('div section div p span::text').get()).replace('/', ''),
                'address': sanitize(apartment.css('div h2 span')[1].css('span::text')[1].get()),
                'squareMeter': sanitize(apartment.css('div ul')[0].css('li')[0].css('span::text')[0].get()),
                'bedrooms': sanitize(apartment.css('div ul')[0].css('li')[1].css('span::text')[0].get()),
                'bathroom': sanitize(apartment.css('div ul')[0].css('li')[2].css('span::text')[0].get()),
                'parkingSpaces': sanitize(apartment.css('div ul')[0].css('li')[3].css('span::text')[0].get())
            }
