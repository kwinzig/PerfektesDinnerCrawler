# -*- coding: utf-8 -*-
import scrapy


class DinnerSpider(scrapy.Spider):
    name = 'dinner'
    allowed_domains = ['www.vox.de/sendungen/das-perfekte-dinner/rezepte']
    start_urls = ['http://www.vox.de/sendungen/das-perfekte-dinner/rezepte/']

    def parse(self, response):
        pass
