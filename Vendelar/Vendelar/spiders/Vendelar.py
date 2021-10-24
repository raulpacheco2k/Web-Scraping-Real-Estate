import scrapy
import re
import unicodedata


class Sanitize:
    @staticmethod
    def clean(text):
        text = unicodedata.normalize('NFKD', text)
        text = re.sub('[^A-Za-z0-9_ ,.]+', '', text)
        text = text.replace('  ', ' ')
        text = text.strip()

        return text


class Vendelar(scrapy.Spider):
    name = 'Vendelar'
    allowed_domains = ['vendelar.com.br']
    start_urls = ['https://www.vendelar.com.br/imoveis?pretensao=comprar&bairros=']

    def parse(self, response, **kwargs):
        properties = response.css('.col-xl-4')
        for property in properties:
            yield {
                'title': Sanitize.clean(property.css('h3::text').get()),
                'price': Sanitize.clean(property.css('.valor::text').get()).replace('R ', '')[0:-2],
                'period': 'Mes',
                'address': Sanitize.clean(property.css('h4::text').get()),
                'squareMeter': Sanitize.clean(property.css('.info-curta li:nth-child(4)::text').get()).replace(' m2', ''),
                'bedrooms': Sanitize.clean(property.css('div').css('ul').css('li::text')[0].get()),
                'bathroom': Sanitize.clean(property.css('div').css('ul').css('li::text')[1].get()),
                'parkingSpaces': Sanitize.clean(property.css('div').css('ul').css('li::text')[2].get()),
                'link': property.css('a::attr(href)')[0].get().replace('//', '')
            }

        try:
            next_page = response.css('.justify-content-center').css('li a::attr(href)')[-1].get().replace('//https://www.vendelar.com.br/', '')
            yield response.follow(url=next_page, callback=self.parse)
        except ValueError:
            self.logger.info('Não há mais páginas.')
