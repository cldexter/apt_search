# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: task.py
   Description: 生成任务列表
   Author: Dexter Chen
   Date：2017-10-11
-------------------------------------------------
"""
import time

from datetime import date, datetime, timedelta
import mongodb_handler as mh
import utilities as ut
import message as msg


def task_endwith():
    pass


def generate_tasks(project, sstr):
    config = get_task_config(project, sstr)
    mh.add_new_task(project, sstr, ut.time_str(
        "full"), config[0], config[1], config[2], 0)


def generate_task_list():  # 项目名称，第一个项目几小时后开始，项目间最小间隔
    pass


def run_task(project, sstr):  # 多少时间后开始运行
    record_number, mrmins, endwith = get_task_config(project, sstr)
    endtime = ut.time_str("full", mrmins)
    msg.msg("crawl pmid", project + sstr, "started", "succ",
            "important", msg.display, msg.log, msg.stat)
    pc.run_pmid_crawler(project, sstr, record_number, endwith, endtime)
    msg.msg("crawl pmid", project + sstr, "finished", "succ",
            "important", msg.display, msg.log, msg.stat)

    msg.msg("crawl detail", project + sstr, "started", "succ",
            "important", msg.display, msg.log, msg.stat)
    dc.run_detail_crawler(project, sstr, record_number)
    msg.msg("crawl detail", project + sstr, "finished", "succ",
            "important", msg.display, msg.log, msg.stat)


if __name__ == '__main__':
    if_task_need()
