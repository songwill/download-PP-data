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

#根据html页面内容，获取价格
def getdayprice(html):
    soup=BeautifulSoup(html)
    t=soup.find("tbody")
    tr=t.find_all("tr")
    td=t.find_all("td")
    plist=[11,15,19,24,28,33,39,43,47,51,56,61,65,69,73,77,81,87,91,95,99,104,
           108,112,116,120,125,129,135,139]
    #splist=[1,11,12,13,14,15,16,17,18,22,23,27,28]  #plist中商品一致项
    s=[]
    for i in plist:
        #print td[i-1].text,type(str(td[i-1].text)),len(td[i-1].text)
        tableprice=str(td[i-1].text.strip('\n'))
        if len(tableprice)<4:       #对形如‘--’的价格，取空值
            adprice=''
        elif len(tableprice)==4 or len(tableprice)==5:     #长度等于4的价格取本身
            adprice=tableprice
        #print adprice
        s.append(adprice)
    dayprice=s
    return dayprice

def getsummary(html):
    soup=BeautifulSoup(html)
    try:
        spp=soup.find('span',text=re.compile(r'.*?PP.*?'))
        sp=spp.parent
        summary=str(sp.text)
        #print summary.strip()
    except:
        patt=re.compile('</TABLE>&nbsp;(.*?)</DIV>',re.S)
        stext=re.findall(patt,html)
        for item in stext:
            summary=unicode(item.strip('&nbsp;'),'gbk')
    return summary


#dateprice=getdayprice(html)

#从本地读取链接并下载价格
pricelist=[]
fr=open('E:/mygit/dec-data/pplinks.txt','r')
lines=fr.readlines()
for i in range(1,346):     #设置下载区间
    linesread=eval(lines[i][:-1])
    readhtml=gethtml(linesread[1])
    try:
        dateprice=getdayprice(readhtml)
        #comment=getsummary(readhtml)
        dateprice.insert(0,linesread[0])#单页面的日期不显示年份，故替换成下载链接的对应的日期
        #dateprice.append(comment)
        pricelist.append(dateprice)
        print linesread[0],"……第…%d…页…" %i
    except:
        pass
        print linesread[0],"%d…页【错误】" %i
fr.close()


#写入CSV,若写入txt，总后总结文字符号较多不便处理
import csv ,codecs     #不导入codecs输出的csv文件中文会显示乱码
csvfile = open('E:/mygit/dec-data/pp_test.csv', 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
s1=['日期','呼炼T30S-京', '神华L5E89-京', '大唐L5E89-京', '大唐L5E89-鲁', '呼炼T30S-鲁', '大唐L5E89-津',
    '大庆T30S-沪', '独山子S1003-沪', '辽通T30S-沪', '武汉T30S-沪', '扬子F401-南京', '镇海T30S-余姚', '独山子S1003-余姚',
    '绍兴T30S-余姚', '大庆T30S-余姚', '富德T30S-余姚', '宁煤1102K-余姚','茂名PPH-T03-广州',
    '湛江T30S-广州', '北海T30S-广州', '广西L5E89-广州', '福联T30S-汕头', '海南T30S-汕头',
    '壳牌HP550J-汕头', '包头L5E89-汕头', '抚顺L5E89-汕头', 'T30S福联-厦门', '1080K福联-厦门', '独山子S1003-武汉', '武汉ST30S-武汉']
writer.writerow(s1)
#for item in pricelist:
#    writer.writerow(item)
writer.writerows(pricelist)
csvfile.close()

#用R读取时x<-read.csv('E:/mygit/dec-data/csv_test.csv',header=T,fileEncoding="UTF-8")，fileEncoding="UTF-8"是关键
