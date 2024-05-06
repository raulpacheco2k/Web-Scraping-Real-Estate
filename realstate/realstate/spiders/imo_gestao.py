import re

import scrapy
import unicodedata


class Sanitize:
    @staticmethod
    def clean(text):
        text = unicodedata.normalize('NFKD', text)
        text = re.sub('[^A-Za-z0-9_ ,.]+', '', text)
        text = text.replace('  ', ' ')
        text = text.strip()

        return text


class ImoGestao(scrapy.Spider):
    name = 'ImoGestao'
    allowed_domains = [
        'vendelar.com.br',
        'imobiliariatubarao.com.br'
    ]
    start_urls = [
        'https://www.vendelar.com.br/imoveis?pretensao=comprar',
        'https://imobiliariatubarao.com.br/imoveis?pretensao=comprar'
    ]

    def parse(self, response, **kwargs):
        properties = response.css('.col-12.col-sm-6.col-xl-4')
        for property in properties:
            yield {
                'Propriedade': Sanitize.clean(property.css('h3::text').get()),
                'Preco': Sanitize.clean(property.css('.valor::text').get()).replace('R ', '')[0:-2].replace(',', '').replace('.', ''),
                'Cidade': Sanitize.clean(property.css('h4::text').get()).split(',')[1].strip(),
                'Bairro': Sanitize.clean(property.css('h4::text').get()).split(',')[0].strip(),
                'Tamanho': Sanitize.clean(property.css('ul > li::text')[-1].get()).replace('m2', '').replace('.', ','),
                'Quartos': Sanitize.clean(property.css('div').css('ul').css('li::text')[0].get()),
                'Banheiros': Sanitize.clean(property.css('div').css('ul').css('li::text')[1].get()),
                'Garagem': Sanitize.clean(property.css('div').css('ul').css('li::text')[2].get()),
                'link': property.css('a::attr(href)')[0].get().replace('//', '')
            }

        try:
            next_page = response.css('.justify-content-center').css('li a::attr(href)')[-1].get()
            yield response.follow(url=next_page, callback=self.parse)
        except ValueError:
            self.logger.info('Não há mais páginas.')
