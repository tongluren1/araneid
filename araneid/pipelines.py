# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import time

from scrapy.conf import settings
import pymysql


class AraneidPipeline(object):
    def process_item(self, item, spider):
        return item

class JianshuPipeline(object):
    def __init__(self, dbpool):
        # 初始化函数
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 从settings.py里获取mysql数据库信息，并定数据编码为utf - 8，以免入库时出错
        dbargs = dict(
            host = settings.get('MYSQL_HOST'),
            port = settings.get('MYSQL_PORT'),
            db = settings.get('MYSQL_DB'),
            user = settings.get('MYSQL_USER'),
            passwd = settings.get('MYSQL_PWD'),
            charset = 'utf8',
            use_unicode = True
        )
        dbpool = pymysql.connect(**dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        print(item)
        if item.get('user_name') != '':
            user_name = item['user_name']
            user_out_url = 'https://www.jianshu.com' + item['user_out_url']
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql = "insert INTO `jianshu_user` ( editor_name, editor_home_url, update_time, add_time ) VALUE ( '" + user_name + "', '" + user_out_url + "', '" + update_time + "', '" + update_time + "' ) ON DUPLICATE KEY UPDATE editor_name = '" + user_name + "', editor_home_url = '" + user_out_url + "', update_time = '" + update_time + "'"

        cursor = self.dbpool.cursor()
        cursor.execute(sql)
        self.dbpool.commit()

        return item