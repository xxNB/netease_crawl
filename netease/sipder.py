# -*- coding: utf-8 -*-
"""
Created on 2017/10/25 下午2:37
@author: SimbaZhang
"""
import requests
import json
import time
from logzero import logger
import pymongo
from netease.encrypt import get_parms
from netease.id_encrypt import get_music_id
from pymongo import MongoClient as mc

client = mc('127.0.0.1', 27017)
db = client['netease']['理想三旬']
db.ensure_index([('comment_id', pymongo.ASCENDING)], unique=True, dropDups=True)

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}

def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content

# 热门评论抓取
def hot_spider(query_list):
    for query in query_list:
        print(query + '\n', '=' * 200 + '\n')
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token=".format(get_music_id(query))
        parms = get_parms()
        params = parms[0]
        encSecKey = parms[1]
        json_text = get_json(url, params, encSecKey)
        json_dict = json.loads(json_text)
        for item in json_dict['hotComments']:
            user = item['user']['nickname']
            content = item['content']
            like = item['likedCount']
            print({'music': query, 'user': user, 'like': like, 'content': content})

# 单首歌曲所有评论爬取
def com_spider(query):
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token=".format(get_music_id(query))
    page = 0
    item_list = []
    while True:
        parms = get_parms(page)
        params = parms[0]
        encSecKey = parms[1]
        json_text = get_json(url, params, encSecKey)
        json_dict = json.loads(json_text)
        for item in json_dict['comments']:
            # print(item)
            user = item['user']['nickname']
            content = item['content']
            like = item['likedCount']
            comment_id = item['commentId']
            res = {'music': query, 'user': user, 'like': like, 'content': content, 'comment_id': comment_id}
            dbItem = db.find_one({'comment_id': res['comment_id']})
            if dbItem:
                continue
            item_list.append(res)
            # print({'music': query, 'user': user, 'like': like, 'content': content})
        time.sleep(1)
        page += 20
        if page % 100 == 0:
            db.insert_many(item_list)
            item_list = []
            logger.info('already download %s' % page)

if __name__ == '__main__':
    query_list = ['晴天', '搁浅', '断桥残雪']
    com_spider('理想三旬')