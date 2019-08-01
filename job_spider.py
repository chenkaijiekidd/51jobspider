#!/usr/bin/python
# --coding:utf-8--

import requests
from lxml import etree
import re
from urllib.parse import urlparse
import os
import csv

key_word = 'python'
location = '广州'
location_dict = {'北京': '010000',
              '上海': '020000',
              '广州': '030200',
              '深圳': '040000',
              '武汉': '180200',
              '西安': '200200',
              '杭州': '080200',
              '南京': '070200',
              '成都': '090200',
              '重庆': '060000',
              '东莞': '030800',
              '珠三角': '01'}

location_num = location_dict[location]
DOMAIN = "jobs.51job.com"
current_page = 1            #当前页数
req_url = 'https://search.51job.com/list/{0},000000,0000,00,9,99,{1},2,{2}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
total_page = float('inf')   #定义无限大
has_next_page = True


session = requests.Session()
session.keep_alive = False

headers = {
    "Host": "search.51job.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0",
    "Accept": "text/css,*/*;q=0.1",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
}


def start_crawl():

    global current_page, total_page, req_url, session, key_word, location_num

    #res = requests.get(req_url.format(current_page), headers=headers)
    res = session.get(req_url.format(location_num, key_word, current_page), headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)

    get_total_page(html)
    job_item_list = []

    item_list = html.xpath("//div[@id='resultList']//div[@class='el']")
    for item in item_list:

        row = []
        #职位名称
        row.append(item.xpath("./p/span/a/text()")[0].strip())
        #公司名称
        row.append(item.xpath("./span[@class='t2']/a/text()")[0].strip())
        #地区
        area = item.xpath("./span[@class='t3']/text()")[0].strip()
        if '-' in area:
            area = area.split('-')[1]
        row.append(area)
        #薪酬 如没有显示薪酬则不抓取
        if len(item.xpath("./span[@class='t4']/text()")) <= 0:
            continue

        salary = item.xpath("./span[@class='t4']/text()")[0].strip()
        if '-' in salary:
            salary = salary.split('-')[1] #获取上限

        try:
            row.append(transfer_salary(str(salary)))
        except ValueError:
            row.append(transfer_salary(str(0)))

        requirement_url = item.xpath("./p/span/a/@href")[0]
        #链接到外部网站的数据，则忽略
        if DOMAIN != urlparse(requirement_url).netloc:
            continue
        #个人要求
        requirement = get_personal_requirement(requirement_url)
        if requirement is not None:
            #工作经验
            row.append(requirement[0])
            #学历
            row.append(requirement[1])


        company_url = item.xpath("./span[@class='t2']/a/@href")[0]
        # 链接到外部网站的数据，则忽略
        if DOMAIN != urlparse(company_url).netloc:
            continue
        #公司信息
        company_info = get_company_info(company_url)
        #公司性质
        row.append(company_info)
        #规模
        #row.append(company_info[1])
        #行业
        #row.append(company_info[2])

        job_item_list.append(row)
        print('crawling item:', row)

    write_to_csv(job_item_list)
    print('******* total page:', total_page, ' and current page:', current_page, '*******')
    current_page += 1


def get_personal_requirement(url):
    '''获取个人要求：学历，工作经验相关'''
    print('crawling personal url:', url)
    #res = requests.get(url, headers=headers)
    res = session.get(url, headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)
    requirement = html.xpath("//div[@class='tHeader tHjob']//p[@class='msg ltype']/text()")
    if requirement is not None and len(requirement) > 0:
        return requirement[1].strip('\xa0'), requirement[2].strip('\xa0')


def get_company_info(url):
    '''获取公司信息：公司性质，人数，行业'''
    print('crawling company url:', url)
    #res = requests.get(url, headers=headers)
    res = session.get(url, headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)
    info = html.xpath("//div[@class='tHeader tHCop']//p[@class='ltype']/@title")
    if info is not None and len(info) > 0:
        return info[0].split('|')[0].strip('\r\n\t\t\t').strip('\xa0')
    return ''


def get_total_page(html):
    '''根据页面信息，返回总共有多少页面'''
    global total_page
    result = html.xpath("//div[@class='dw_page']//div[@class='p_in']/span[@class='td'][1]/text()")
    total_page = int(re.findall(r"\d+\.?\d*", result[0])[0])


def has_next_page():
    '''查看是否还有下一个页面'''
    global current_page, total_page
    return True if current_page <= total_page else False


def transfer_salary(salary_str):
    '''转换薪酬'''
    salary_num = float(re.findall(r"\d+\.?\d*", salary_str)[0])
    if '/' in salary_str:
        if '月' in salary_str and '千' in salary_str:
            return salary_num * 1000
        elif '月' in salary_str and '万' in salary_str:
            return salary_num * 10000
        elif '年' in salary_str and '万' in salary_str:
            return salary_num * 10000 / 12
        elif '年' in salary_str and '千' in salary_str:
            return salary_num * 1000 / 12
        else:
            return 0.00
    return 0.00


def write_to_csv_header():

    with open('job_item.csv', 'a') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(['职位名称', '公司名称', '地区', '薪酬', '工作经验', '学历', '公司性质'])


def write_to_csv(job_item_list):

    with open('job_item.csv', 'a') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(job_item_list)


if __name__ == '__main__':

    if os.path.exists('job_item.csv'):
        os.remove('job_item.csv')
    write_to_csv_header()
    while has_next_page():
        start_crawl()
