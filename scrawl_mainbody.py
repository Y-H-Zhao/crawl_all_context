# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 09:42:53 2017

@author: ZYH
"""

import requests
from bs4 import BeautifulSoup
import re
import chardet

#url随意替换
#url ='http://mil.news.sina.com.cn/china/2017-04-05/doc-ifycwymx3854291.shtml'
#gbk
url='http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw39329/userobject82aw117458.html'
#url='http://www.heb.chinanews.com/hwkhb1/20180420374934.shtml'
#utf
#url='http://www.jiangxi.gov.cn/xzx/jxyw/sxyw/201804/t20180420_1440333.html'
#url='http://epaper.syd.com.cn/syrb/html/2018-04/20/content_180132.htm?div=-1'
page = requests.get(url)
#这里需要根据网页编码的不同情况进行判断
mychar = chardet.detect(page.content)
bianma = mychar['encoding'] #获取编码
#UTF-8-sig or UTF-8 or utf-8 or utf-8-sig
if bianma[:2]=='ut' or bianma[:2]=='UT':
    page.encoding = 'utf-8'
#gbk or GBK or GB2312 or gb2312
elif bianma[:2]=='gb' or bianma[:2]=='GB':
    page.encoding = 'gbk'
#解析网页
soup = BeautifulSoup(str(page.text), 'html.parser')

def countchn(string):
    pattern = re.compile(u'[\u1100-\uFFFDh]+?')
    result = pattern.findall(string)
    chnnum = len(result)            #list的长度即是中文的字数
    possible = chnnum/len(str(string))  #possible = 中文字数/总字数
    return (chnnum, possible)

part = soup.select('div')
def findtext(part):  
    global paragraph_f
    length = 50000000
    l = []
    for paragraph in part:
        chnstatus = countchn(str(paragraph))
        possible = chnstatus[1]
        if possible > 0.15:         
            l.append(paragraph)
    l_t = l[:]
    #这里需要复制一下表，在新表中再次筛选，要不然会出问题，跟Python的内存机制有关
    for elements in l_t:
        chnstatus = countchn(str(elements))
        chnnum2 = chnstatus[0]
        if chnnum2 < 300:    
        #最终测试结果表明300字是一个比较靠谱的标准,当然可以根据实际需要就行修改
            l.remove(elements)
        elif len(str(elements))<length:
            length = len(str(elements))
            paragraph_f = elements.text
    return(paragraph_f)
article=findtext(part)
print(article)
with open('{0}.txt'.format('time_or_title'),'w',encoding='UTF-8') as f:
    f.write(article)
print('save.{}'.format('time_or_title'))
