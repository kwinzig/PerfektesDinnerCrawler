# -*- coding: utf-8 -*-
import scrapy


class DinnerSpider(scrapy.Spider):
    name = 'dinner'
    start_urls = ['http://www.vox.de/sendungen/das-perfekte-dinner/rezepte/']

    def parse(self, response):
        recipe_urls = response.css('.recipe-results .rtli-row .rtli-large-2 a::attr(href)').extract()
        for recipe_url in recipe_urls:
            yield scrapy.Request(response.urljoin(recipe_url), callback=self.parse_recipe)
        next_url_div = response.css('.voxde-pagination-list .rtli-btn-link')
        next_url = next_url_div[2].css('a::attr(href)').extract()
        if len(next_url) > 0:
            yield scrapy.Request(response.urljoin(next_url[0]), callback=self.parse)

    def parse_recipe(sel, response):
        pass