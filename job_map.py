# -*- coding: utf-8 -*-
"""
@Time : 2019-08-12 11:24
@Author : kidd
@Site : http://www.bwaiedu.com/
@File : test.py
@公众号: 蓝鲸AI教育 bwaiedu
"""

from pyecharts import options as opts
from pyecharts.charts import Geo, Map
from pyecharts.globals import ChartType, SymbolType
from cities import Data
import csv

areas = ["天河区", "黄埔区", "荔湾区", "番禺区", "越秀区", "花都区", "海珠区", "从化区", "增城区", "南沙区", "白云区"]
values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def geo_effectscatter() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="广州")
        .add(
            "geo",
            [list(z) for z in zip(areas, values)],
            type_=ChartType.EFFECT_SCATTER,
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Geo-EffectScatter"),
                         visualmap_opts=opts.VisualMapOpts(is_piecewise=True),)
    )
    return c


def map_visualmap() -> Map:
    c = (
        Map()
        .add("python职位数", [list(z) for z in zip(areas, values)], "广州")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-VisualMap（分段型）"),
            visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
        )
    )
    return c

def load_data():
    with open('job_item.csv', 'r') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            area = row[2]
            if area in Data.areas:
                values[areas.index(area)] = values[areas.index(area)] + 1
    map_visualmap().render()

if __name__ == '__main__':
    # c = map_visualmap()
    # c.render()
    load_data()