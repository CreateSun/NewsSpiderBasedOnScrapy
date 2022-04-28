# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YangshiproItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    image2 = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    count = scrapy.Field()
    ext_field = scrapy.Field()
    image = scrapy.Field()
    focus_date = scrapy.Field()
    image3 = scrapy.Field()
    brief = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    timeline = scrapy.Field()
    origin = scrapy.Field()
    category = scrapy.Field()
