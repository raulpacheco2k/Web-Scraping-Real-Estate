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


class ImobiliariaTubarao(scrapy.Spider):
    name = 'ImobiliariaTubarao'
    allowed_domains = ['imobiliariatubarao.com.br']
    start_urls = ['https://imobiliariatubarao.com.br/imoveis?pretensao=alugar&tipos=1&cidade=4218707']

    def parse(self, response, **kwargs):
        properties = response.css('.imovel_ideal_home')

        for property in properties:
            datails = property
            property = property.css('.trans')

            yield {
                'title': Sanitize.clean(property.css('h2 span::text').get()),
                'price': Sanitize.clean(property.css('h4 strong span::text').get()).replace('R ', '')[0:-2],
                'period': 'Mes',
                'address': Sanitize.clean(property.css('h4')[1].css('span::text').get()),
                'squareMeter': Sanitize.clean(property.css('ul li::text')[3].get().strip().split(' ')[0]),
                'bedrooms': Sanitize.clean(property.css('ul li::text')[0].get().strip().split(' ')[0]),
                'bathroom': Sanitize.clean(property.css('ul li::text')[1].get().strip().split(' ')[0]),
                'parkingSpaces': Sanitize.clean(
                    property.css('div').css('ul').css('li::text')[2].get().strip().split(' ')[0]),
                'link': self.allowed_domains[0] + datails.css('a::attr(href)')[1].get()
            }

        try:
            next_page = response.css('#accordion nav ul li')[3].css('a::attr(href)').get()
            yield response.follow(url=next_page, callback=self.parse)
        except ValueError:
            self.logger.info('Não há mais páginas.')
