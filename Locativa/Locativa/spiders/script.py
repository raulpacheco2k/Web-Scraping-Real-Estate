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


class Locativa(scrapy.Spider):
    name = 'Locativa'
    allowed_domains = ['https://www.locativa.com.br']
    start_urls = [
        'https://www.locativa.com.br/alugar?sidebar=S&grade=&itens=32&ordem=&temporada=&pageNum_RSBusca=0&totalRows_RSBusca=0&cod_imovel=&tipo%5B%5D=APARTAMENTO&tipo%5B%5D=CASA&tipo%5B%5D=KITINETI&cidade%5B%5D=TUBARAO&metragem=1&area_menor=&area_maior=&valor_menor=&valor_maior=']

    @staticmethod
    def search(property, identifier):
        if property.css(identifier).get():
            identifier = Sanitize.clean(property.css(identifier).get())
        else:
            'Sem dados'

        return identifier

    def parse(self, response, **kwargs):
        properties = response.css('#ajax-content .mb20')

        for property in properties:
            yield {
                'title': Sanitize.clean(property.css('h2::text').get()) + ' ' + Sanitize.clean(
                    property.css('h2 span::text').get()),
                'price': Sanitize.clean(property.css('.borda-5px::text').get()).replace('R ', ''),
                'period': 'Mes',
                'address': '-',
                'squareMeter': self.search(property, '.area::text'),
                'bedrooms': self.search(property, '.dormi::text'),
                'bathroom': self.search(property, '.banho::text'),
                'parkingSpaces': self.search(property, '.garagem::text'),
                'link': self.allowed_domains[0] + '/' + property.css('a::attr(href)').get()
            }

        try:
            next_page = response.css('#accordion nav ul li')[3].css('a::attr(href)').get()
            yield response.follow(url=next_page, callback=self.parse)
        except ValueError:
            self.logger.info('Não há mais páginas.')
