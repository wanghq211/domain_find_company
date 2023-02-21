import requests
from lxml import etree
import threadpool
import xlwt
import urllib3
import os
from urllib import parse
urllib3.disable_warnings()



def scan(domain):
    try:
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Referer":f"https://icp.chinaz.com/{domain}"
        }
        data = f"keyword={domain}"
        url = f'https://icp.chinaz.com/{domain}'
        req = requests.post(url,headers=header,data=data,verify=False)
        response = etree.HTML(req.text)
        company = response.xpath('//a[@id="companyName"]/text()')
        title = response.xpath('//li[@class="clearfix"]/p[@class="Wzno"]/text()')[0]
        result[company[0]] = title
        p = open('result.txt','a')
        p.write(str(company[0]) + ':' + title + '\n')
    except:
        pass
if __name__ == '__main__':
    n = 0
    result = {}
    domain_list = []
    f = open('domain.txt','r')
    for i in f.readlines():
        domain = parse.urlparse(i).netloc
        domain_list.append(domain.strip('\n'))
    if os.path.exists('result.txt'):
        k = open('result.txt','w')
        k.truncate()
    if os.path.exists('result.txt.csv'):
        j = open('result.csv','w')
        k.truncate()
    pool = threadpool.ThreadPool(5)
    reqs = threadpool.makeRequests(scan,domain_list)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet(u'结果', cell_overwrite_ok=True)
    sheet1.write(0, 0, '公司')
    sheet1.write(0, 1, '网站')
    for key,value in result.items():
        if n < len(result):
            sheet1.write(n+1,0,key)
            sheet1.write(n+1,1,str(value))
            n += 1
        else:
            break
    book.save('result.csv')
    print('结束！结果保存在./result.csv中')
