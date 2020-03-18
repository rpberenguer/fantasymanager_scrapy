# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
import logging

settings = get_project_settings() 

class MongoDBPipeline(object):

    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )

        self.db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        collection = self.db[type(item).__name__.lower()]
        collection.insert(dict(item))
        return item
