Na pasta no site que você deseja executar o seguinte comando `scrapy crawl VivaReal -o apartments.json`, lembre-se de
antes de executar o comando inserir a URL que você deseja coletar dentro da variável `start_urls` dentro
de `/Example/Example/spiders/Example.py`.

> Abstenho-me de qualquer uso mal-intencionado do script!

# Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker run -it -p 8050:8050 --rm scrapinghub/splash
```

# Run

```bash
scrapy runspider realstate/realstate/spiders/imo_gestao.py -o properties.csv && scrapy runspider realstate/realstate/spiders/vista.py -o properties.csv
```