#!/usr/bin/python
# --coding:utf-8--

from multiprocessing import Process, Queue, Manager
import requests
from lxml import etree
import re
from job_item import JobItem
import csv
#from bs4 import BeautifulSoup
#from bs4 import element
from pyecharts.charts import Map

current_page = 1            #当前页数
req_url = 'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,' + str(current_page) + '.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0,0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
total_page = float('inf')   #定义无限大
has_next_page = True

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


def get_main_info(url):
    pass

def get_personal_requirement(index, url, share_list):
    '''获取个人要求：学历，工作经验相关'''
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)
    requirement = html.xpath("//div[@class='tHeader tHjob']//p[@class='msg ltype']/text()")
    #return requirement[1].strip('\xa0'), requirement[2].strip('\xa0')
    share_list[index].append(requirement[1].strip('\xa0'))
    share_list[index].append(requirement[2].strip('\xa0'))


def get_company_info(index, url, share_list):
    '''获取公司信息：公司性质，人数，行业'''
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)
    info = html.xpath("//div[@class='tHeader tHCop']//p[@class='ltype']/@title")[0].split('|')
    #return info[0].strip('\r\n\t\t\t').strip('\xa0'), info[1].strip('\xa0'), info[2].strip('\xa0')
    share_list[index].append(info[0].strip('\r\n\t\t\t').strip('\xa0'))
    share_list[index].append(info[1].strip('\r\n\t\t\t').strip('\xa0'))
    share_list[index].append(info[2].strip('\r\n\t\t\t').strip('\xa0'))


def get_total_page(html):
    '''根据页面信息，返回总共有多少页面'''
    global total_page
    result = html.xpath("//div[@class='dw_page']//div[@class='p_in']/span[@class='td'][1]/text()")
    total_page = int(re.findall(r"\d+\.?\d*", result[0])[0])


def has_next_page():
    '''查看是否还有下一个页面'''
    global current_page, total_page
    return True if current_page < total_page else False


def write_to_csv(job_item_list):

    with open('job_item.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(job_item_list)


def start_crawl(url):

    q = Queue()
    write_csv_proc = Process(target=get_main_info, args=(url) )


    global current_page, total_page

    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    html = etree.HTML(res.text)

    get_total_page(html)
    current_page += 1
    job_item_list = []

    with Manager() as manager:
        share_list = manager.list()
        proc_list = []

        item_list = html.xpath("//div[@id='resultList']//div[@class='el']")
        for index, item in enumerate(item_list):

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
            #薪酬
            salary = item.xpath("./span[@class='t4']/text()")[0].strip()
            if '-' in salary:
                salary = salary.split('-')[1]
            row.append(salary)

            share_list.append(row)

            personal_url = item.xpath("./p/span/a/@href")[0]
            personal_proc = Process(target=get_personal_requirement, args=(index, personal_url, share_list))
            personal_proc.start()
            proc_list.append(personal_proc)

            company_url = item.xpath("./span[@class='t2']/a/@href")[0]
            company_proc = Process(target=get_company_info, args=(index, company_url, share_list))
            company_proc.start()
            proc_list.append(company_proc)


        for proc in proc_list:
            proc.join()

        write_to_csv(share_list)
        print('total page:', total_page, ' and current page:', current_page)


if __name__ == '__main__':

    while has_next_page():
        start_crawl(req_url)
