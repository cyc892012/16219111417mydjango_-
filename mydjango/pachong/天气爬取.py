from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getweather():
    resp=urlopen('http://www.weather.com.cn/weather/101210701.shtml')
    soup=BeautifulSoup(resp,'html.parser')
    tagDate=soup.find('ul', class_="t clearfix")
    dates=tagDate.h1.string

    tagToday=soup.find('p', class_="tem")
    try:
        temperatureHigh=tagToday.span.string
    except AttributeError as e:
        temperatureHigh=tagToday.find_next('p', class_="tem").span.string

    temperatureLow=tagToday.i.string
    weather=soup.find('p', class_="wea").string

    tagWind=soup.find('p',class_="win")
    winL=tagWind.i.string

    weather_list={ 'date' : dates, 'win' : winL, 'tmpLow' : temperatureLow, 'tmpHigh' : temperatureHigh, 'weather' : weather}
    return weather_list
print(getweather())
