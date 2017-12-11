# -*- coding: utf-8 -*-
import scrapy
from Sina.items import SinaItem
import os

class SinanewsSpider(scrapy.Spider):
    name = 'sinanews'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []
        #大类标题和Urls
        parentUrls = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()
        parentTitles = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()

        #小类标题和urls
        subUrls = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()
        subTitles = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()

        #爬取所有大类
        for i in range(0,len(parentTitles)):
            #指定大类目录路径
            parentFilename = './Data/'+parentTitles[i]

            #如果目录不存在,创建目录
            if (not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            #爬取小类
            for j in range(0,len(subUrls)):
                item = SinaItem()
                #保存大类的title和urls
                print(parentTitles[i],i)
                item['parentTitle'] = parentTitles[i]
                item['parentUrls'] = parentUrls[i]

                #检测小类的url是否以同类别大类Url开头,如果是返回True
                if_belong = subUrls[j].startswith(item['parentUrls'])
                #如果属于本大类,将存储目录放在本大类目录下
                if if_belong:
                    subFilename = parentFilename+'/'+subTitles[j]

                    #目录不存在建立
                    if not os.path.exists(subFilename):
                        os.makedirs(subFilename)

                    #存储小类url title 和filename 字段
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] = subTitles[j]
                    item['subFilename'] = subFilename

                    items.append(item)

        for item in items:
            yield scrapy.Request(url = item['subUrls'],meta={'meta_1': item}, callback=self.second_parse)
    #对于返回的小类url,再进行递归请求
    def second_parse(self,response):
        #提取每次response的meta数据
        meta_1 = response.meta['meta_1']
        #提取小类里所有子链接
        sonUrls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0,len(sonUrls)):
            # 检查每个链接是否以大类url开头、以.shtml结尾，如果是返回True
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            # 如果属于本大类，获取字段值放在同一个item下便于传输
            if(if_belong):
                item = SinaItem()
                item['parentTitle'] =meta_1['parentTitle']
                item['parentUrls'] =meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        # 发送每个小类下子链接url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2': item}, callback=self.detail_parse)


    def detail_parse(self,response):
        item = response.meta['meta_2']
        content = ""
        head = response.xpath('//h1[@id="main_title"]/text()').extract()
        content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()

        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one

        item['head']= head
        item['content']= content.replace('\u3000',' ').replace('\xa0',' ')

        yield item

