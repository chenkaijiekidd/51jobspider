#!/usr/bin/python
# --coding:utf-8--

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# from matplotlib import font_manager
# a = sorted([f.name for f in font_manager.fontManager.ttflist])
# for i in a:
#     print(i)

print(matplotlib.matplotlib_fname())
job_list = pd.read_csv('job_item.csv', dtype={'职位名称': str, '公司名称': str, '地区': str, '薪酬': float, '工作经验': str, '学历': str, '公司性质': str})
print(job_list['薪酬'].sum())
print(job_list['薪酬'].mean())
print(job_list.groupby('工作经验').size())
print(job_list.groupby('学历').size())
print(job_list.groupby('地区').size())
print(job_list.groupby('公司性质').size())

exit()


area_data = pd.read_csv('area.csv', dtype={'地区': str, '招聘数量': int})
index = area_data['地区']
values = area_data['招聘数量']
plt.bar(index, values)
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()

# education_data = pd.read_csv('education.csv', dtype={'学历': str, '招聘数量': int})
# index = education_data['学历']
# values = education_data['招聘数量']
# plt.bar(index, values)
# plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签  # 用来正常显示中文标签
# plt.show()

education_data = pd.read_csv('education.csv', dtype={'学历': str, '招聘数量': int})
plt.figure(figsize=(6, 9))
plt.pie(education_data['招聘数量'], labels=education_data['学历'], autopct='%.2f')
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()


experience_data = pd.read_csv('experience.csv', dtype={'经验': str, '招聘数量': int})
plt.figure(figsize=(6, 9))
plt.pie(experience_data['招聘数量'], labels=experience_data['经验'], autopct='%.2f')
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()

company_data = pd.read_csv('company.csv', dtype={'公司性质': str, '招聘数量': int})
plt.figure(figsize=(6, 9))
plt.pie(company_data['招聘数量'], labels=company_data['公司性质'], autopct='%.2f')
plt.rcParams['font.sans-serif'] = ['Heiti TC'] #用来正常显示中文标签
plt.show()





