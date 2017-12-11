# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    #大类标题和链接
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    #小类的标题和url
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    #小类目录存储路径
    subFilename = scrapy.Field()

    #小类下的子链接
    sonUrls = scrapy.Field()

    #文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()


