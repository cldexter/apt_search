#! /usr/bin/env python
# coding=utf-8
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name: mongodb_handler.py
   Description: 处理一切与mongodb对接的工作
   Author: Dexter Chen
   Date：2017-09-28
-------------------------------------------------
"""

#引入numpy库和matplotlib库
import numpy as np
import matplotlib.pyplot as plt

# 定义等高线图的横纵坐标x，y
#从左边取值为从 -3 到 3 ，各取5个点，一共取 5*5 = 25 个点
x = np.linspace(-3, 3, 5)
y = np.linspace(-3, 3, 5)
# 将原始数据变成网格数据
X, Y = np.meshgrid(x, y)

# 各地点对应的高度数据
#Height是个 5*5 的数组，记录地图上 25 个点的高度汇总
Height = [[0,0,1,2,2],[0,-2,-2,1,5],[4,2,6,8,1],[3,-3,-3,0,5],[1,-5,-2,0,3]]

# 填充颜色
plt.contourf(X, Y, Height, 10, alpha = 0.6, cmap = plt.cm.hot)
# 绘制等高线
C = plt.contour(X, Y, Height, 10, colors = 'black', linewidth = 0.5)
# 显示各等高线的数据标签
plt.clabel(C, inline = True, fontsize = 10)
plt.show()