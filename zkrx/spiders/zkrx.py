import scrapy
from zkrx.items import ZkrxItem

class zkrx(scrapy.Spider):
    name = 'zkrx'
    start_urls = ["http://www.shmeea.edu.cn/20150603/20150603.htm"]

    def parse(self, response):
        self.school_name = response.xpath("//table[@class='MsoNormalTable']//a/text()").extract()
        self.links = response.xpath("//table[@class='MsoNormalTable']//a/@href").extract()
        for link in self.links:
            yield scrapy.Request(link, callback=self.get_data)


    def get_data(self, response):
        #包含“姓名”关键字的table
        tables = response.xpath("//table[*[td='姓名']]")
        url = response.url
        for table in tables:
            if ('推荐' in table.xpath("tr[1]/td/text()").extract()[0]):
                item = ZkrxItem()
                item['name'] = table.xpath("tr[position()>2]/td[3]/text()").extract()
                item['sn'] = table.xpath("tr[position()>2]/td[2]/text()").extract()
                item['cat'] = ['推荐']*len(table.xpath("tr/td[3]/text()"))
                item['school'] = [self.school_name[self.links.index(url)]]*len(table.xpath("tr/td[3]/text()"))
                yield item
            else:
                item = ZkrxItem()
                item['name'] = table.xpath("tr/td[3]/text()").extract()
                item['sn'] = table.xpath("tr/td[2]/text()").extract()
                item['cat'] = ['自荐']*len(table.xpath("tr/td[3]/text()"))
                item['school'] = [self.school_name[self.links.index(url)]]*len(table.xpath("tr/td[3]/text()"))
                yield item
