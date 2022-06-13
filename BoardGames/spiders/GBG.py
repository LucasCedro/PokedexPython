import csv
import scrapy
import os

class GbgSpider(scrapy.Spider):
    name = 'pokedex'
    start_urls = ['https://www.pokemon.com/br/pokedex']

    if os.path.exists("pokedex.csv"):
        os.remove("pokedex.csv")

    #Primeira parte do código. Aqui buscamos cada link de cada pokemon
    def parse(self, response):
        for link in response.xpath('//div//ul//li//a[contains(@href,"/us/pokedex")]/@href').extract():  # preciso pegar apenas dos itens [10] ate o [914]
            URL = f"https://www.pokemon.com{link}"
            yield scrapy.Request(URL.replace("/us/", "/br/"), callback=self.parse_text)

    #Segunda parte do código. Aqui buscamos as informações de cada pokemon propriamente dito
    def parse_text(self, response):

        if len(response.css('.pokedex-pokemon-pagination-title div::text').get().split()) == 2:
            nome = response.css('.pokedex-pokemon-pagination-title div::text').get().split()[0] + ' ' + response.css('.pokedex-pokemon-pagination-title div::text').get().split()[1]
        if len(response.css('.pokedex-pokemon-pagination-title div::text').get().split()) == 1:
            nome = response.css('.pokedex-pokemon-pagination-title div::text').get().split()[0].replace("['",'').replace("'","")

        pokemon = {
            'nome': nome,
            'numero': response.css('.pokedex-pokemon-pagination-title .pokemon-number::text').get().replace('Nº', ''),
            'altura': response.css('.attribute-value::text').getall()[0], #não fiz um loop nessa parte pois nao preciso dos outros dados do array
            'peso': response.css('.attribute-value::text').getall()[1],
            'habilidade': response.css('.attribute-value::text').getall()[-1],
            'caracteristica': response.css('.column-7.push-7 .attribute-title+ .attribute-value::text').get(),
            'tipo': response.xpath('//div[@class="dtm-type"]//ul//li[contains(@class,"background-color")]//a/text()').get(),
            'imagem': response.css('.profile-images .active ::attr(src)').get()

        }

        with open('pokedex.csv', 'a', newline='', encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, pokemon.keys())
            dict_writer.writerows([pokemon])
        yield pokemon




# ATENÇÃO #
# Para criar o JSON use o seguinte comando: scrapy crawl pokedex -O pokedex.json