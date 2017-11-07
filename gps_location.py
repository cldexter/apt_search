#! /usr/bin/env python
# coding=utf-8
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import requests
import mongodb_handler as mh
import message as msg


def geocodeG(address):  # 使用高德API
    par = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    GPS = answer['geocodes'][0]['location'].split(",")
    return GPS[0], GPS[1]


def get_geocode_baidu(city, address):  # 使用百度API
    base = "http://api.map.baidu.com/geocoder/v2/?city=" + city + "&address=" + \
        address + "&output=json&ak=wMPAp888f2qXr4bNAj0x5nCFK0eIPquu"
    response = requests.get(base)
    answer = response.json()
    if answer['status'] == 0:
        lat = answer['result']['location']['lat']
        lng = answer['result']['location']['lng']
        mh.add_location(city, address, lat, lng)
        return lat, lng
    else:
        return 0, 0


def loc_2_geocode(number):  # 地址转为geocode
    address_set = mh.read_address_many(number)  # 先提取没有geocode的这些
    for address in address_set:
        location_record = mh.read_location(address[1], address[2])  # 读取本地有无记录
        if location_record:  # 如果有记录
            geocode = location_record[0], location_record[1]  # 直接用记录
            msg.msg("location info",
                    address[2], "local retrieve", "succ", "info", msg.display)
        else:  # 如果本地没有记录
            geocode = get_geocode_baidu(address[1], address[2])  # 到百度api抓取
            msg.msg("location info",
                    address[2], "web retrieve", "succ", "info", msg.display)
        mh.update_geocode(address[0], geocode[1], geocode[0])  # 把地理记录录入数据库


if __name__ == '__main__':
    loc_2_geocode(5000)
