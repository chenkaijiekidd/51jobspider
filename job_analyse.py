# -*- coding: utf-8 -*-
"""
@Time : 2019-08-12 11:24
@Author : kidd
@Site : http://www.bwaiedu.com/
@File : test.py
@公众号: 蓝鲸AI教育 bwaiedu
"""

import pandas as pd
import matplotlib.pyplot as plt

#print(matplotlib.matplotlib_fname())
job_list = pd.read_csv('job_item.csv', dtype={'职位名称': str, '公司名称': str, '地区': str, '薪酬': float, '工作经验': str,
                                              '学历': str, '公司性质': str})
#print(job_list['薪酬'].sum())
#print(job_list['薪酬'].count())
print('平均薪酬：', job_list['薪酬'].mean(), '元')

#学历统计
education_dic = dict(job_list.groupby('学历').size())
key_list = []
key_list.extend(education_dic.keys())

for key in key_list:
    if '招' in key:
        del education_dic[key]

education_labels = education_dic.keys()
education_values = education_dic.values()
plt.pie(education_values, labels=education_labels, autopct='%1.1f%%', shadow=False, startangle=150)
plt.title("学历统计")
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()

#工作经验统计
experience_dic = dict(job_list.groupby('工作经验').size())
key_list = []
key_list.extend(experience_dic.keys())
#去掉不包含年的工作经验选项
for key in key_list:
    if '年' not in key:
        del experience_dic[key]

experience_labels = experience_dic.keys()
experience_values = experience_dic.values()
plt.pie(experience_values, labels=experience_labels, autopct='%1.1f%%', shadow=False, startangle=150)
plt.title("工作经验统计")
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()

#工作地区统计
area_dict = dict(job_list.groupby('地区').size())
key_list = []
key_list.extend(area_dict.keys())
area_labels = area_dict.keys()
area_values = area_dict.values()
plt.pie(area_values, labels=area_labels, autopct='%1.1f%%', shadow=False, startangle=150)
plt.title("工作地区统计")
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()

#公司性质统计
company_dic = dict(job_list.groupby('公司性质').size())
key_list = []
key_list.extend(company_dic.keys())

company_labels = company_dic.keys()
company_values = company_dic.values()
plt.pie(company_values, labels=company_labels, autopct='%1.1f%%', shadow=False, startangle=150)
plt.title("公司性质统计")
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()


# print(job_list.groupby('学历').size())
# print(job_list.groupby('公司性质').size())
# education_data = pd.read_csv('education.csv', dtype={'学历': str, '招聘数量': int})
# plt.figure(figsize=(6, 9))
# plt.pie(education_data['招聘数量'], labels=education_data['学历'], autopct='%.2f')
# plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
# plt.show()
#
#
# experience_data = pd.read_csv('experience.csv', dtype={'经验': str, '招聘数量': int})
# plt.figure(figsize=(6, 9))
# plt.pie(experience_data['招聘数量'], labels=experience_data['经验'], autopct='%.2f')
# plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
# plt.show()
#
# company_data = pd.read_csv('company.csv', dtype={'公司性质': str, '招聘数量': int})
# plt.figure(figsize=(6, 9))
# plt.pie(company_data['招聘数量'], labels=company_data['公司性质'], autopct='%.2f')
# plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
# plt.show()





