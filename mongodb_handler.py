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
    if data_type in ["apartment", "price", "log", "location"]:
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

# 增加log


def add_new_log(when, who, identifier, action, result, info_type):
    data = {"ctime": when, "who": who, "identifier": identifier,
            "action": action, "result": result, "info_type": info_type}
    get_db('log').insert_one(data)

# 读取地址


def read_address_many(number):
    record = []
    for data in get_db("apartment").find({"status": 1}).limit(number):
        record.append([data["apt_id"], data["city"], data['disctrict'] +
                       data['sub_district'] + data["street"] + data["zone"]])
    return record


def update_geocode(apt_id, apt_lat, apt_lng):
    get_db("apartment").update({"apt_id": apt_id}, {
        "$set": {"status": 2, "apt_lat": apt_lat, "apt_lng": apt_lng}})


def add_location(city, address, lat, lng):
    data = {"city": city, "address": address,
            "lat": lat, "lng": lng}
    get_db("location").insert_one(data)


def read_location(city, address):
    data = get_db("location").find_one({"city": city, "address": address})
    if data:
        return data['lat'], data['lng']


def upgrade_status():
    get_db("apartment").update({'_id': {'$exists': True}}, {
        '$set': {"apt_type": "二手"}}, multi=True)


if __name__ == "__main__":
    # print read_address_many(1)
    # upgrade_status()
    add_location("广州", "暨南大学", 0, 0)
    print read_location("广州","暨南大学")