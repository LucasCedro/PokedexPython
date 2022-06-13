import scrapy
import csv
import os

class PokestatsSpider(scrapy.Spider):
    name = 'pokestats'
    start_urls = ['https://pokemondb.net/pokedex/all']

    if os.path.exists("pokestats.csv"):
        os.remove("pokestats.csv")

    #Primeira parte do código. Aqui buscamos cada link de cada pokemon
    def parse(self, response):
        for link in response.xpath('//tr//td[@class="cell-name"]//a/@href').extract():
            URL = f"https://pokemondb.net{link}"
            yield scrapy.Request(URL, callback=self.parse_text)

    #Segunda parte do código. Aqui buscamos as informações de cada pokemon propriamente dito
    def parse_text(self, response):

        pokestats = {
            'nome': response.xpath('//h1/text()').get(),
            'numero': response.xpath('//td//strong/text()').get(),

            'hp_base': response.xpath('//tbody//tr[contains(th,"HP")]//td[@class="cell-num"]/text()').getall()[0],
            'hp_min': response.xpath('//tbody//tr[contains(th,"HP")]//td[@class="cell-num"]/text()').getall()[1],
            'hp_max': response.xpath('//tbody//tr[contains(th,"HP")]//td[@class="cell-num"]/text()').getall()[2],

            'attack_base': response.xpath('//tbody//tr[contains(th,"Attack")]//td[@class="cell-num"]/text()').getall()[0],
            'attack_min': response.xpath('//tbody//tr[contains(th,"Attack")]//td[@class="cell-num"]/text()').getall()[1],
            'attack_max': response.xpath('//tbody//tr[contains(th,"Attack")]//td[@class="cell-num"]/text()').getall()[2],

            'defesa_base': response.xpath('//tbody//tr[contains(th,"Defense")]//td[@class="cell-num"]/text()').getall()[0],
            'defesa_min': response.xpath('//tbody//tr[contains(th,"Defense")]//td[@class="cell-num"]/text()').getall()[1],
            'defesa_max': response.xpath('//tbody//tr[contains(th,"Defense")]//td[@class="cell-num"]/text()').getall()[2],

            'sp_attack_base': response.xpath('//tbody//tr[contains(th,"Sp. Atk")]//td[@class="cell-num"]/text()').getall()[0],
            'sp_attack_min': response.xpath('//tbody//tr[contains(th,"Sp. Atk")]//td[@class="cell-num"]/text()').getall()[1],
            'sp_attack_max': response.xpath('//tbody//tr[contains(th,"Sp. Atk")]//td[@class="cell-num"]/text()').getall()[2],

            'sp_defesa_base': response.xpath('//tbody//tr[contains(th,"Sp. Def")]//td[@class="cell-num"]/text()').getall()[0],
            'sp_defesa_min': response.xpath('//tbody//tr[contains(th,"Sp. Def")]//td[@class="cell-num"]/text()').getall()[1],
            'sp_defesa_max': response.xpath('//tbody//tr[contains(th,"Sp. Def")]//td[@class="cell-num"]/text()').getall()[2],

            'speed_base': response.xpath('//tbody//tr[contains(th,"Speed")]//td[@class="cell-num"]/text()').getall()[0],
            'speed_min': response.xpath('//tbody//tr[contains(th,"Speed")]//td[@class="cell-num"]/text()').getall()[1],
            'speed_max': response.xpath('//tbody//tr[contains(th,"Speed")]//td[@class="cell-num"]/text()').getall()[2],
        }

        with open('pokestats.csv', 'a', newline='', encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, pokestats.keys())
            dict_writer.writerows([pokestats])
        yield pokestats

# ATENÇÃO #
# Para criar o JSON use o seguinte comando: scrapy crawl pokedex -O pokedex.json