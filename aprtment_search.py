#! /usr/bin/env python
# coding=utf-8
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import sys
import os
import time
import re
import requests
import agents
from lxml import etree
import mongodb_handler as mh
import utilities as ut
import dictionary as di
from BeautifulSoup import BeautifulSoup


apt_id_set = []


default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def generate_url():
    url_set = []
    url_begin = "http://gz.centanet.com/ershoufang/t1"
    url_end = "/?key=%E5%B9%BF%E5%B7%9E"
    url = url_begin + url_end
    opener = requests.Session()
    doc = opener.get(url, timeout=5, headers=agents.get_header()).text
    soup = BeautifulSoup(doc)
    content = soup.findAll(name="span", attrs={"class": "fred fTahoma"})
    total_number = str(content[0])[27:-7]
    page_number = int(total_number) / 25 + 1
    i = 0
    for i in range(0, page_number):
        url_each = url_begin + "g" + str(i + 1) + url_end
        url_set.append(url_each)
    return url_set


url = "http://gz.centanet.com/ershoufang/t1"


def get_apt_id_set():
    global apt_id_set
    apt_id_set = mh.read_apt_id_all()


def generate_detail(url):
    global apt_id_set
    opener = requests.Session()
    doc = opener.post(url, timeout=20).text
    selector = etree.HTML(doc.encode("utf-8"))
    content_element = selector.xpath("//*[@class=\"house-item clearfix\"]/@id")
    content_number = len(content_element)
    title_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/h4/a")
    zone_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[1]/a")
    apt_type_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[1]/span[2]")
    apt_area_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[1]/span[4]")
    apt_floor_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[2]/span[1]")
    apt_direction_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[2]/span[2]")
    apt_decoration_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[2]/span[3]")
    apt_year_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[2]/span[4]")
    apt_location_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[1]/p[3]/span")
    apt_total_price_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[2]/p[1]/span")
    apt_average_price_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[2]/p[1]/span")
    zone_average_price_element = selector.xpath(
        "//*[@class=\"house-item clearfix\"]/div[2]/p[3]")
    i = 0
    for i in range(0, content_number):
        apt_id = content_element[i]
        if not apt_id in apt_id_set:
            title = title_element[i].xpath('string(.)')
            zone = zone_element[i].xpath('string(.)')
            apt_type = apt_type_element[i].xpath('string(.)')
            if apt_type:
                br_number = apt_type[0]
                lr_number = apt_type[2]
            apt_area = apt_area_element[i].xpath('string(.)')
            apt_floor = apt_floor_element[i].xpath('string(.)')
            if apt_floor:
                apt_floor_s = apt_floor.split("/")
                if apt_floor_s[0]:
                    apt_floor_type_s = apt_floor_s[0]
                    apt_floor_type = ut.dict_replace(
                        apt_floor_type_s, di.dict_floor_type)
                if apt_floor_s[1]:
                    apt_floor_number = apt_floor_s[1][0:-1]
            apt_direction = apt_direction_element[i].xpath('string(.)')
            if apt_direction:
                apt_direction_en = ut.dict_replace(
                    apt_direction, di.dict_direction)
            apt_decoration = apt_decoration_element[i].xpath('string(.)')
            if apt_decoration:
                apt_decoration_en = ut.dict_replace(
                    apt_decoration, di.dict_decoration)
            apt_year = apt_year_element[i].xpath('string(.)')
            if apt_year:
                apt_year = apt_year[0:4]
            apt_location = apt_location_element[i].xpath('string(.)')
            if apt_location:
                apt_location_s = apt_location.split(" ")
                district_s = apt_location_s[0]
                if district_s:
                    district_s_s = district_s.split("-")
                    district = district_s_s[0]
                    sub_district = district_s_s[1]
                street = apt_location_s[1]
            apt_total_price = apt_total_price_element[i].xpath('string(.)')
            apt_average_price = apt_average_price_element[i].xpath('string(.)')
            zone_average_price = zone_average_price_element[i].xpath(
                'string(.)')
            apartment_record = {
                "ctime": ut.time_str("full"),
                "apt_id": apt_id,
                "title": title,
                "zone": zone,
                # "apt_type": apt_type,
                "br_number": br_number,
                "lr_number": lr_number,
                # "apt_floor": apt_floor,
                "apt_floor_type": apt_floor_type,
                "apt_floor_number": apt_floor_number,
                # "apt_direction": apt_direction,
                "apt_direction_en": apt_direction_en,
                # "apt_decoration": apt_decoration,
                "apt_decoration_en": apt_decoration_en,
                "apt_year": apt_year,
                # "apt_location": apt_location,
                "disctrict": district,
                "sub_district": sub_district,
                "street": street
            }
            price_record = {
                "ctime": ut.time_str("full"),
                "apt_id": apt_id,
                "apt_total_price": apt_total_price,
                "apt_average_price": apt_average_price,
                "zone_average_price": zone_average_price
            }
            mh.add_record(apartment_record, "apartment")
            mh.add_record(price_record, "price")
            apt_id_set.append(apt_id)
            print "saved record: " + apt_id
        else:
            print "skipped record: " + apt_id


if __name__ == "__main__":
    get_apt_id_set()
    url_list  = generate_url()
    for url in url_list:
        generate_detail(url)
