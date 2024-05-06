import re

import scrapy
import unicodedata


class Sanitize:
    @staticmethod
    def clean(text, is_address=False):
        text = unicodedata.normalize('NFKD', text)
        text = re.sub('[^A-Za-z0-9_ ,.]+', '', text)
        text = text.strip()

        if is_address is True:
            text = text.split(',')
            cidade, bairro, estado = text
            text = f"{bairro.strip()}, {cidade.strip()}"

        return text


class Vista(scrapy.Spider):
    name = 'Vista'
    allowed_domains = ['imobiliariaradar.com.br']
    start_urls = [
        #'https://imobiliariaradar.com.br/busca/?finalidade=Aluguel'
         'https://imobiliariaradar.com.br/busca/?finalidade=Venda'
    ]

    def parse(self, response, **kwargs):
        properties = response.css('.col-xs-12.col-sm-6.col-md-4.animation')
        for property in properties:
            yield {
                'Propriedade': Sanitize.clean(
                    property.css('.col-xs-12.col-sm-6.col-md-4.animation::attr(data-categoria)').get()),
                'Preco':
                    Sanitize.clean(property.css('.label.price::text').get()).replace('R', '').replace('.', '').split(
                        ',')[0].strip(),
                'Cidade': Sanitize.clean(property.css('address::text').get(), True).split(',')[1].strip(),
                'Bairro': Sanitize.clean(property.css('address::text').get(), True).split(',')[0].strip(),
                'Tamanho': '' if property.css('div').css('.pull-left').css('li::text').get() is None else
                property.css('div').css('.pull-left').css('li::text').extract()[1].strip(),
                'Quartos': property.css('[title="Dormitórios"]::text').extract()[1].strip() if property.css(
                    '[title="Dormitórios"]::text').extract() else '',
                'Banheiros': property.css('[title="Banheiro"]::text').extract()[1].strip() if property.css(
                    '[title="Banheiro"]::text').extract() else '',
                'Garagem': property.css('[title="Vaga"]::text').extract()[1].strip() if property.css(
                    '[title="Vaga"]::text').extract() else '',
                'link': property.css('a::attr(href)').get()
            }

        try:
            next_page = response.css('.pagination').css('li a::attr(href)')[-1].get()
            yield response.follow(url=next_page, callback=self.parse)
        except ValueError:
            self.logger.info('Não há mais páginas.')
