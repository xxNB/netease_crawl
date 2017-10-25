# -*- coding: utf-8 -*-
"""
Created on 2017/10/25 下午2:37
@author: SimbaZhang
"""
import requests
import json
from netease.encrypt import get_parms
from netease.id_encrypt import get_music_id

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

def spider(query_list):
    for query in query_list:
        print(query + '\n', '=' * 200 + '\n')
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token=".format(get_music_id(query))
        params = get_parms()[0]
        encSecKey = get_parms()[1]
        json_text = get_json(url, params, encSecKey)
        json_dict = json.loads(json_text)
        for item in json_dict['hotComments']:
            user = item['user']['nickname']
            content = item['content']
            like = item['likedCount']
            print({'music': query, 'user': user, 'like': like, 'content': content})

if __name__ == '__main__':
    query_list = ['晴天', '搁浅', '断桥残雪']
    spider(query_list=query_list)