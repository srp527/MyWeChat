# -*- coding:utf-8 -*- 
__author__ = 'SRP'

import pymongo

from settings import MONGO_DB,MONGO_URL,MONGO_TABLE

class MongoPipeline(object):

    conn = pymongo.MongoClient(MONGO_URL)

    def to_mongo(self,item):
        collection_name = MONGO_TABLE
        db = self.conn[MONGO_DB]
        # db.authenticate("username", "password")
        db[collection_name].insert(dict(item))
        # db[collection_name].update(dict(item))

    def from_mongo(self):
        collection_name = MONGO_TABLE
        db = self.conn[MONGO_DB]
        # db.authenticate("username", "password")
        collection = db.get_collection(collection_name)
        document = collection.find()
        return document

    def close_mongo(self):
        self.conn.close()

