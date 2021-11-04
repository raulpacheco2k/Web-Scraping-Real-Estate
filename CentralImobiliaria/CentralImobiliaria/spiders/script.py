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


class CentralImobiliaria(scrapy.Spider):
    name = 'CentralImobiliaria'
    allowed_domains = ['https://www.cilcentralimobiliaria.com.br']
    start_urls = [
        'https://www.cilcentralimobiliaria.com.br/pesquisa/listar/ad/1/imovel_tipo_id/1/imovel_transacao_id/2/cidade_id/8742/#col-pesquisa'
    ]

    @staticmethod
    def search(property, identifier):
        if property.css(identifier).get():
            identifier = Sanitize.clean(property.css(identifier).get())
        else:
            'Sem dados'

        return identifier

    def parse(self, response, **kwargs):
        properties = response.css('.item')

        for property in properties:
            yield {
                'title': Sanitize.clean(property.css('figcaption').xpath('normalize-space()').get()),
                'price': self.search(property, 'p strong::text').replace('R ', ''),
                'period': 'Mes',
                'address': Sanitize.clean(property.css('p strong::text')[1].get()).replace(' Tubarao', ''),
                'squareMeter': property.css('tr td')[0].css('p')[1].css('b::text').get() if len(property.css('tr td')) == 3 else 'Sem dados',
                'bedrooms': property.css('tr td')[0].css('p')[1].css('b::text').get() if len(property.css('tr td')) == 2 else property.css('tr td')[1].css('p')[1].css('b::text').get(),
                'bathroom': 'Sem dados',
                'parkingSpaces': property.css('tr td')[1].css('p')[1].css('b::text').get() if len(property.css('tr td')) == 2 else property.css('tr td')[2].css('p')[1].css('b::text').get(),
                'link': self.allowed_domains[0] + '/' + property.css('a::attr(href)').get()
            }

        # try:
        #     next_page = response.css('#accordion nav ul li')[3].css('a::attr(href)').get()
        #     yield response.follow(url=next_page, callback=self.parse)
        # except ValueError:
        #     self.logger.info('Não há mais páginas.')
