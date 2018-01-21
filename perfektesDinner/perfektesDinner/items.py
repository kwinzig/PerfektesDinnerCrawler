# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PerfektesdinnerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class RecipeItem(scrapy.Item):
    recipe_id = scrapy.Field()
    recipe_name = scrapy.Field()
    recipe_preparation = scrapy.Field()
    recipe_infos = scrapy.Field()
    reicpe_ingredient_meal_parts = scrapy.Field()


class RecipeInfos(scrapy.Item):
    info_preparation_time = scrapy.Field()
    info_difficulty = scrapy.Field()
    info_price_range = scrapy.Field()


class NutritionFacts(scrapy.Item):
    kj_kcal = scrapy.Field()
    protein = scrapy.Field()
    carbohydrates = scrapy.Field()
    fat = scrapy.Field()


class IngredientMealPart(scrapy.Item):
    mealpart_name = scrapy.Field()
    mealpart_ingredients = scrapy.Field()


class Ingredient(scrapy.Item):
    ingredient_name = scrapy.Field()
    ingredient_amount = scrapy.Field()
    ingredient_unit = scrapy.Field()