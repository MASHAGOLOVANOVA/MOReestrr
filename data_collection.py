import os
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.request import urlopen
from lxml import etree
from fake_useragent import UserAgent
from random import randint


# Для получения веб-страницы
def get_dataset(url):
    headers = {"User-Agent": UserAgent().chrome}
    response = requests.get(url, headers=headers)
    html = response.text
    res = all_about_response(response)
    if res[:29] == 'https://www.list-org.com/bot?':
        return None
    response = urlopen(write(html))
    htmlparser = etree.HTMLParser()
    treee = etree.parse(response, htmlparser)
    return treee


def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def all_about_response(response):
    print(response)
    print(response.url)
    for key, value in response.request.headers.items():
        print(key + ": " + value)
    for resp in response.history:
        print(resp.status_code, resp.url)
    return response.url


# Запись страницы html в файл
def write(html):
    with open('C:/Users/kysya/PycharmProjects/pythonProject2/clinic_html.txt', 'w', encoding="utf-8") as f:
        f.write(html)
    local = 'file:///C:\\Users\\kysya\\PycharmProjects\\pythonProject2\\clinic_html.txt'
    return local


def get_dat(url, search):
    headers = {"User-Agent": UserAgent().chrome}
    params = {'query': search}
    response = requests.get(url, headers=headers, params=params)
    response = requests.get(response.url, headers=headers)
    all_about_response(response)
    html = response.text
    response = urlopen(write(html))
    htmlparser = etree.HTMLParser()
    treee = etree.parse(response, htmlparser)
    return treee


def pare(url):
    tree = get_dataset(url)
    return tree.xpath('//div[contains(@class, "mt-2")]/a[contains(@class, "btn")]/@href')[0]


def page_parse(first):
    l = []
    for i in range(first, first+49, 2):
        p1 = pare('https://www.list-org.com/search?type=all&work=on&work=on&okved=86&sort=&page='+str(i))
        time.sleep(5)
        p2 = pare('https://www.list-org.com/search?type=all&work=on&work=on&okved=86&sort=&page='+ str(i+1))
        time.sleep(5)
        ne = 'https://www.list-org.com/excel_list.php?ids='+p1[20:]+','+p2[20:]
        print(f'{i}-{i+1}')
        print(ne)
        l.append(ne)
    return l


def get_pos(url):
    tree = get_dataset(url)
    if tree == None:
        return 'bot'
    if tree.xpath('//td/span[contains(@class, "upper")]/text()') == [] :
        return ''
    return tree.xpath('//td/span[contains(@class, "upper")]/text()')[0]


def parse_urls(urls , first):
    list = []
    for i in range (first, len(urls), 1):
        while (True):
            try:
                time.sleep(randint(5,20))
                pos=get_pos(urls[i])
                if pos=='bot':
                    time.sleep(120)
                    raise Exception
                print(pos)
                list.append(pos)
                print(i)
                break
            except:
                print(f'{i} didnt got!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                df = pd.DataFrame()
                df['positions']= pd.Series(list)
                df.to_excel("output.xlsx")
                time.sleep(30)
        if i==len(urls)-1:
            df = pd.DataFrame()
            df['positions']= pd.Series(list)
            df.to_excel("output.xlsx")


df = pd.read_excel('output_new_with_region.xlsx', sheet_name='Sheet1')
urls = df['Ссылка на www.list-org.com'].to_list()

parse_urls(urls, 94)
