from urllib import parse
import re
import time
from selenium import webdriver
import os
from lxml import etree
import MySQLdb

conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mydjango",charset="utf8")
cur=conn.cursor()
cur.execute("TRUNCATE TABLE jdtest")

#如果没有配置chromedriver.exe的环境变量，要写完整路径
chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
#chromedriver = "chromedriver.exe"
browser = webdriver.Chrome(chromedriver)

url = "https://www.jd.com/"
browser.get(url)
time.sleep(1)
#手机号登录
phoneLogin = browser.find_element_by_xpath('//*[@id="key"]')
phoneLogin.send_keys('华为')

time.sleep(1)
# 搜索
#//*[@id="search"]/div/div[2]/button
btnNext = browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
btnNext.click()

def getitem(n):
    time.sleep(3)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 执行JavaScript实现网页下拉倒底部
    page = browser.page_source
    html = etree.HTML(page)
    links = html.xpath("//*[@id='J_goodsList']/ul[@class='gl-warp clearfix']")
    for link in links:
        # 通过xpath获取商品链接
        #//*[@id="J_goodsList"]/ul/li[5]/div/div[1]/a
        verlink = link.xpath("./li[@class='gl-item']/div[@class='gl-i-wrap']/div[@class='p-img']/a/@href")
        verlink = [parse.urljoin(browser.current_url,i) for i in verlink]
        #通过xpath获取商品价格
        #//*[@id="J_goodsList"]/ul/li[60]/div/div[3]/strong/i
        price = link.xpath("./li[@class='gl-item']/div[@class='gl-i-wrap']/div[@class='p-price']/strong")
        price = [item.xpath('string(.)') for item in price]
        #通过xpath获取商品名称
        #//*[@id="J_goodsList"]/ul/li[8]/div/div[4]/a/em
        name=link.xpath("//div[@class='gl-i-wrap']/div[4]/a/em")
        name = [item.xpath('string(.)') for item in name]
    for i in range(len(verlink)-1):
        Name=name[i]
        Href=verlink[i]
        Price=price[i]
        print(Name)
        cur.execute("insert into jdtest(name,href,price) values(\"%s\",\"%s\",\"%s\")"%(Name,Href,Price))


    btnnext = browser.find_element_by_class_name("pn-next")
    btnnext.click()

    n=n+1
    if n==10:
        return
    getitem(n)

    
getitem(0)
conn.commit()
conn.close()

