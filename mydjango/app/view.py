#coding=UTF-8
import requests
import MySQLdb
from django.shortcuts import render
import pymysql
from getdata import top250
from getdata import weather
def index(request):
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='123456',
        db='mydjango',
        charset='utf8')
    # cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cur = conn.cursor()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sqlfindtop250 ="SELECT * from movie_dbtop250"
    sqlfindjdtest="SELECT * from jdtest"

    #top250.updateTop250()  #重新爬取top250数据
    cur.execute(sqlfindtop250)
    listTop250=cur.fetchall()

    cur.execute(sqlfindjdtest)
    listjdtest=cur.fetchall()

    cur.close()

    conn.close()

    #获取天气
    weatherdir = weather.getweather()
    #返回字典到html
    return render(request,'index.html',{'top250':listTop250, 'weather':weatherdir, 'jdtest':listjdtest})