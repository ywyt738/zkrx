# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class ZkrxPipeline(object):
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host='172.31.27.40', user='root', password='123456', database='test')
            self.cursor = self.conn.cursor()
            print('连接数据库成功!')
        except:
            print('连接数据库失败!')

    def process_item(self, item, spider):
        # print("开始写入数据")
        for i in range(1,len(item)):
            param = (item['name'][i], item['sn'][i], item['cat'][i], item['school'][i])
            sql = "insert into zkrx (name, sn, cat, school) values(%s,%s,%s,%s)"
            self.cursor.execute(sql, param)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print("执行完毕")
