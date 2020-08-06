# coding:utf-8

import scrapy
import os

class NovelSpider(scrapy.Spider):

    count = 0
    name = "ns"
    domain = "http://www.xxxxx.com"

    root = "F:/"

    start_urls = ["http://www.xxxxx.com/newslist/xxx.html"]

    def parse(self, response):

        links = response.xpath('//div[@class="box list channel"]/ul/li/a/@href').getall()

        for link in links:
            yield scrapy.Request(url=self.domain + link,callback=self.download)

        # next page
        next_page = response.xpath('//div[@class="pagination"]/a/@href').getall()[-2]
        if next_page == "javascript:;":
            return
        yield scrapy.Request(url=self.domain + next_page,callback=self.parse)

    def download(self,response):

        titles = response.xpath('//div[@class="page_title"]/text()').extract()
        if len(titles) > 0:
            title = titles[0]
        
            img_list = response.xpath('//div[@class="content"]/p/img/@src').getall()

            for url in img_list:
                name = str(url).rsplit('/')[-1]
                yield scrapy.Request(url=url,callback=self.download_img, meta={'path':title,'name':name})
        
    
    def download_img(self,response):
        path = response.meta['path']
        name = response.meta['name']
        root_path = self.root + "/" + path
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        
        with open(root_path + "/" + name,"ab+") as f:
            f.write(response.body)

        print("\033[32m" + path + "/" + name + " Write Success...\033[0m")