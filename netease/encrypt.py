# -*- coding: utf-8 -*-
"""
Created on 2017/10/25 下午11:40
@author: SimbaZhang
"""
from Crypto.Cipher import AES
from netease.id_encrypt import get_music_id
import base64
import requests
import json

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}

first_param = {'rid':'', 'offset':'0', 'total':'true', 'limit':'20', 'csrf_token':'',}
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    first_param = {'rid': '', 'offset': '0', 'total': 'true', 'limit': '20', 'csrf_token': '', }
    first_param = json.dumps(first_param)
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(bytes_str(h_encText), second_key, iv)
    return bytes_str(h_encText)

def bytes_str(byte):
    return byte.decode('utf-8')


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    # print(type(text))
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content

def get_parms():
    params = get_params()
    encSecKey = get_encSecKey()
    return (params, encSecKey)



