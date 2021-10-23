import scrapy


class ApartmentsForRentInTubarao(scrapy.Spider):
    name = 'VivaReal'
    start_urls = ['https://www.vivareal.com.br/aluguel/santa-catarina/tubarao/apartamento_residencial/']

    def _parse(self, response, **kwargs):
        for aparments in response.css('a.js-card-title'):
            yield {
                'title': aparments.css('div h2 span::text')[0].get().strip(),
                'address': aparments.css('div h2 span')[1].css('span::text')[1].get().strip(),
                'squareMeter': aparments.css('div h2 span')[1].css('span::text')[1].get().strip(),
            }
