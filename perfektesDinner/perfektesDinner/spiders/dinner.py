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
        #if len(next_url) > 0:
        #    yield scrapy.Request(response.urljoin(next_url[0]), callback=self.parse)

    def parse_recipe(self, response):
        recipe_name = response.css(".article-headline::text").extract_first()
        self.get_ingredients(response)

    def get_ingredients(self, response):
        ingredients_table = response.css(".voxde-recipe-table")
        for ingredient_row in ingredients_table[0].css("tr"):
            if ingredient_row.css('tr::attr(rel)'):
                ingredient_data = ingredient_row.css('td')
                ingredient_name = ingredient_data[0].css('::text').extract_first()
                ingredient_amount = ingredient_data[1].css('span::text').extract_first()
                ingredient_unit = ""
                if len(ingredient_data[1].css('::text').extract()) > 2:
                    ingredient_unit = str.strip(ingredient_data[1].css('::text').extract()[2])
                print(ingredient_name, ingredient_amount, ingredient_unit)
            else:
                meal_part = ingredient_row.css("th::text").extract_first()
                print(meal_part)