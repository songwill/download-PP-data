#Author:songwill
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
from bs4 import BeautifulSoup

#获取html文档
def gethtml(url):
    request=urllib2.Request(url)
    response=urllib2.urlopen(request)
    html=response.read()
    return html


#"国内主要市场PP拉丝收盘价格（20150807）"
url='http://www.dce.com.cn/portal/info?cid=1392950687100&iid=1438938123100&type=CMS.NEWS'
#"国内主要市场PP拉丝收盘价格（20140224）"
#url='http://www.dce.com.cn/portal/info?cid=1392950687100&iid=1393232018100&type=CMS.NEWS'
html=gethtml(url)
soup=BeautifulSoup(html)
t=soup.find("tbody")
tr=t.find_all("tr")
td=t.find_all("td")
plist=[11,15,19,24,28,33,39,43,47,51,56,61,65,69,73,77,81,87,91,95,99,104,
       108,112,116,120,125,129,135,139]
#splist=[1,11,12,13,14,15,16,17,18,22,23,27,28]  #2014年与15年plist中商品名称一致项
s=[]
for i in plist:
    #print td[i-1].text,type(str(td[i-1].text)),len(td[i-1].text)
    tableprice=str(td[i-3].text.strip('\n'))
    s.append(tableprice)
for i in range(30):
    print "'%s'," %(s[i].decode('utf-8')),    #print 的东西后面加逗号可以使内容同行输出  
    
