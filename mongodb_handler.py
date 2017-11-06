# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: mongodb_handler.py
   Description: 处理一切与mongodb对接的工作
   Author: Dexter Chen
   Date：2017-09-28
-------------------------------------------------
"""

from pymongo import *
import utilities as ut

client = MongoClient('mongodb://localhost:27017/')  # 固定的不要变动
# 获取各个集合路径; 注意这里的db不是database，是collection


def get_db(data_type):
    if data_type in ["apartment","price"]:
        database = client["apartment"][data_type]
    else:
        database = "error"
    return database


# 通用操作部分
def count_record(data_type):
    number = get_db(data_type).count()
    return number


def read_record_all(data_type):  # 获取某集合所有数据
    records = []
    if count_record(data_type) > 0:
        for record in get_db(data_type).find():
            records.append(record)
    return records


def add_record(data, data_type):
    get_db(data_type).insert_one(data)


# 读取所有apt_id
def read_apt_id_all():
    records = []
    for record in get_db("apartment").find():
        records.append(record["apt_id"])
    return records





if __name__ == "__main__":
    pass
