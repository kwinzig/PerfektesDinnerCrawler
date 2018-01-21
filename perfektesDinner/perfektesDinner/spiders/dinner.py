# -*- coding: utf-8 -*-
import scrapy
from perfektesDinner.items import *


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
        recipe_id = response.url.split('/')[6]
        recipe_name = response.css(".article-headline::text").extract_first()
        ingredients = self.get_ingredients(response)
        recipe_infos = self.get_recipe_infos(response)
        nutrition_facts = self.get_recipe_nutrition_facts(response)
        preparation_text = self.get_preparation_text(response)

        recipe = RecipeItem()
        recipe['recipe_id'] = recipe_id
        recipe['recipe_name'] = recipe_name
        recipe['recipe_infos'] = recipe_infos
        recipe['recipe_nutrition_facts'] = nutrition_facts
        recipe['recipe_preparation_text'] = preparation_text
        recipe['reicpe_ingredients'] = ingredients
        yield recipe

    def get_ingredients(self,response):
        person_quantity = response.css('input::attr(data-base-qty)').extract_first()
        ingredients_table = response.css(".voxde-recipe-table")
        ingredient_meal_parts = []
        ingredient_meal_part = IngredientMealPartItem()
        ingredient_meal_part['mealpart_name'] = "None"
        ingredient_meal_part_ingredients = []
        for ingredient_row in ingredients_table[0].css("tr"):
            if ingredient_row.css('tr::attr(rel)'):
                ingredient_data = ingredient_row.css('td')
                ingredient_name = ingredient_data[0].css('::text').extract_first()
                ingredient_amount = ingredient_data[1].css('span::text').extract_first()
                ingredient_unit = ""
                if len(ingredient_data[1].css('::text').extract()) > 2:
                    ingredient_unit = str.strip(ingredient_data[1].css('::text').extract()[2])
                ingredient = IngredientItem()
                ingredient['ingredient_name'] = ingredient_name
                ingredient['ingredient_amount'] = ingredient_amount
                ingredient['ingredient_unit'] = ingredient_unit
                ingredient_meal_part_ingredients.append(ingredient)
            else:
                if len(ingredient_meal_part_ingredients) > 0:
                    ingredient_meal_part['mealpart_ingredients'] = {item['ingredient_name']:item for item in ingredient_meal_part_ingredients}
                    ingredient_meal_parts.append(ingredient_meal_part)
                meal_part_name = ingredient_row.css("th::text").extract_first()
                ingredient_meal_part = IngredientMealPartItem()
                ingredient_meal_part['mealpart_name'] = meal_part_name
                ingredient_meal_part_ingredients = []

        ingredient_meal_part['mealpart_ingredients'] = {item['ingredient_name']:item for item in ingredient_meal_part_ingredients}
        ingredient_meal_parts.append(ingredient_meal_part)
        ingredients = IngredientsItem()
        ingredients['person_quantity'] = person_quantity
        ingredients['ingredient_meal_parts'] = {item['mealpart_name']:item for item in ingredient_meal_parts}

        return ingredients

    def get_recipe_infos(self, response):
        info_table = response.css(".voxde-recipe-table")[1]
        info_table_rows = info_table.css("tr")
        difficulty_td = info_table_rows[0].css("td")
        difficulty = difficulty_td[1].css("::text").extract_first()
        preparation_time_td = info_table_rows[1].css("td")
        preparation_time = preparation_time_td[1].css("::text").extract_first()
        price_category_td = info_table_rows[2].css("td")
        price_category = price_category_td[1].css("span::text").extract_first()

        recipe_infos = RecipeInfosItem()
        recipe_infos['info_preparation_time'] = preparation_time
        recipe_infos['info_difficulty'] = difficulty
        recipe_infos['info_price_range'] = price_category

        return recipe_infos

    def get_recipe_nutrition_facts(self, response):
        nutrition_table = response.css(".voxde-recipe-table")[2]
        nutrition_table_row = nutrition_table.css("tr")
        kj_kcal_td = nutrition_table_row[0].css("td")
        kj_kcal = kj_kcal_td[1].css("::text").extract_first()
        protein_td = nutrition_table_row[1].css("td")
        protein = protein_td[1].css("::text").extract_first()
        carbohydrates_td = nutrition_table_row[2].css("td")
        carbohydrates = carbohydrates_td[1].css("::text").extract_first()
        fat_td = nutrition_table_row[3].css("td")
        fat = fat_td[1].css("::text").extract_first()

        nutrition_facts = NutritionFactsItem()
        nutrition_facts['kj_kcal'] = kj_kcal
        nutrition_facts['protein'] = protein
        nutrition_facts['carbohydrates'] = carbohydrates
        nutrition_facts['fat'] = fat

        return nutrition_facts

    def get_preparation_text(self, response):
        rtli_large_12_divs = response.css(".rtli-large-12")
        preparation_div = rtli_large_12_divs[9]
        preparation_text = preparation_div.css("h4::text, p::text").extract()

        return preparation_text


