# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    volume = scrapy.Field()
    rating = scrapy.Field()

