# -*- coding: utf-8 -*-
"""
@Time : 2019-08-12 11:24
@Author : kidd
@Site : http://www.bwaiedu.com/
@File : test.py
@公众号: 蓝鲸AI教育 bwaiedu
"""

class JobItem:


    def __init__(self):
        self._title = None
        self._company = None
        self._area = None
        self._salary = 0.00
        self._experience = 0
        self._education = None
        self._nature = None #公司性质
        self._scale = None #规模
        self._industry = None #行业

    def __str__(self):
        return self._title + '/' + self._company





