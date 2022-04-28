# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os

from itemadapter import ItemAdapter


class YangshiproPipeline:
    def __init__(self):
        if not os.path.exists('./yangshi_news.csv'):
            # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
            self.f = open("yangshi_news.csv", "a", newline="", encoding='utf-8')
            # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
            self.fieldnames = ["id",
                               "timeline",
                               "title",
                               "category",
                               "keywords",
                               "origin",
                               "image",
                               "focus_date",
                               "brief",
                               "url",
                               "image2",
                               "content",
                               "image3",
                               "count",
                               "ext_field"
                               ]
            # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
            self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
            # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
            self.writer.writeheader()
        else:
            self.f = open("yangshi_news.csv", "a", newline="", encoding='utf-8')
            self.fieldnames = ["id",
                               "timeline",
                               "title",
                               "category",
                               "keywords",
                               "origin",
                               "image",
                               "focus_date",
                               "brief",
                               "url",
                               "image2",
                               "content",
                               "image3",
                               "count",
                               "ext_field"
                               ]
            self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)

    '''
        重写父类方法
        该仅仅在爬虫开始时调用一次
    '''

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.writer.writerow(item)
        print('保存成功', item['category'], item['title'])
        return item  # 传递给下一个执行的管道类

    def close_spider(self, spider):
        print('结束爬虫...')
        self.f.close()
