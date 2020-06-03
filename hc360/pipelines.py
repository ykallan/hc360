# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
pymysql.install_as_MySQLdb()


class Hc360Pipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            database='scrapy',
            user='root',
            passwd='root',
            charset='utf8',
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        self.cursor.execute('''INSERT INTO hc360(mobile, tele, cont_person, com_name) VALUES(%s, %s, %s, %s)''',
                            (item['mobile'], item['tele'], item['cont_person'], item['com_name']))
        self.conn.commit()
        return item

    def close(self, spider):
        # self.cursor.close()
        # self.conn.close()
        pass
