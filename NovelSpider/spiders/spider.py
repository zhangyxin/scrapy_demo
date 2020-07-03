# coding:utf-8

import scrapy


class NovelSpider(scrapy.Spider):

    count = 0
    name = "ns"
    domain = "https://www.xxx.cc"

    index = 7

    start_urls = ["https://www.xxx.cc/"]

    def parse(self, response):

        links = response.xpath('//div[@id="main"]/a/@href').getall()

        for link in links:
            yield scrapy.Request(url=self.domain + link,callback=self.download)

        # next page
        next_page = response.xpath('//div[@class="page_wrap_inner"]/ul/li/a/@href').getall()[self.index]
        if next_page == "javascript:;":
            return
        self.index = 8
        yield scrapy.Request(url=self.domain + next_page,callback=self.parse)

    def download(self,response):

        title = response.xpath('//h1/text()').extract()
        title = str(title[0]).strip(' ')
        contents = response.xpath('//div[@class="novel-wrap"]/div/p/text()').getall()

        with open("../../" + title + ".txt","a+",encoding="utf-8") as f:
            for content in contents:
                if len(content) > 12:
                    f.write(content)
                    f.write("\r\n")
        self.count = self.count + 1
        print(title + " Write Success....All is [" ,self.count ,"] ..")