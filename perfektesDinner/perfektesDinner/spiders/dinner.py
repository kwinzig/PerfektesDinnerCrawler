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
        self.get_recipe_infos(response)
        self.get_recipe_nutrition_facts(response)
        self.get_preparation_text(response)

    def get_ingredients(self,response):
        person_quantity = response.css('input::attr(data-base-qty)').extract_first()
        print(person_quantity)
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

    def get_recipe_infos(self, response):
        info_table = response.css(".voxde-recipe-table")[1]
        info_table_rows = info_table.css("tr")
        difficulty_td = info_table_rows[0].css("td")
        difficulty = difficulty_td[1].css("::text").extract_first()
        preparation_time_td = info_table_rows[1].css("td")
        preparation_time = preparation_time_td[1].css("::text").extract_first()
        price_category_td = info_table_rows[2].css("td")
        price_category = price_category_td[1].css("span::text").extract_first()
        print(difficulty, preparation_time, price_category)

    def get_recipe_nutrition_facts(self, response):
        nutrition_table = response.css(".voxde-recipe-table")[2]
        nutrition_table_row = nutrition_table.css("tr")
        kj_kcal_td = nutrition_table_row[0].css("td")
        kj_kcal = kj_kcal_td[1].css("::text").extract_first()
        protein_td = nutrition_table_row[1].css("td")
        protein = protein_td[1].css("::text").extract_first()
        carbonhydrates_td = nutrition_table_row[2].css("td")
        carbonhydrates = carbonhydrates_td[1].css("::text").extract_first()
        fat_td = nutrition_table_row[3].css("td")
        fat = fat_td[1].css("::text").extract_first()
        print(kj_kcal, protein, carbonhydrates, fat)

    def get_preparation_text(self, response):
        rtli_large_12_divs = response.css(".rtli-large-12")
        preparation_div = rtli_large_12_divs[9]
        preparation_text = preparation_div.css("h4::text, p::text").extract()
        print(preparation_text)


