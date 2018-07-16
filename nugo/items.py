# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Homework(scrapy.Item):
    subject = scrapy.Field()
    name = scrapy.Field()
    submission_status = scrapy.Field()
    submission_graded = scrapy.Field()
    submission_date = scrapy.Field()
    left_time = scrapy.Field()
    last_modification = scrapy.Field()
    grade = scrapy.Field()
