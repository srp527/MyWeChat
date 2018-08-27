# -*- coding:utf-8 -*- 
__author__ = 'SRP'

import json

import codecs

from to_mongo import MongoPipeline as db

data = db()
a = data.from_mongo()

# print(list(a))
# for i in a:
#     print(i)

friends_file = './data/friends.json'
with codecs.open(friends_file,encoding='utf-8') as f:
    friends = json.load(f)
    print(friends)