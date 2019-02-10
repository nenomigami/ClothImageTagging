# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 19:03:01 2019

@author: nenom
"""
#에러 케이스 1: 데이터 col이 다를 경우
#에러 케이스 2: 하다가 모종의 이유로 중지가 될 경우
#에러 케이스 3: 하다가 데이터가 바뀌는 경우
from bs4 import BeautifulSoup as bs
import csv
import urllib.request
import urllib.error
import requests
import re

HOME_PAGE = "https://www.shein.com"
SAVE_POINT = open("save_point.txt","w")
PATTERN = re.compile("c-goodsli j-goodsli j-goodsli-[0-9]{6} col-lg-3 col-sm-4 col-xs-6")
IMAGE_PATH = 'E:\\HY\\HY\\like Legendary\\6 - ClothImageTagging\\Data\\images'
CSV_PATH = 'E:\\HY\\HY\\like Legendary\\6 - ClothImageTagging\\Data'
MASS = [u"\xa0","SHEIN"]
FILENAME_F = "prodURL_F.txt"
FILENAME_M = "prodURL_M.txt"

def get_categoryURL(sex):
    #카테고리별로 url을 리턴한다
    """
    Arguments:
        sex - 0 : women, 1: men
    
    return:
        queue - list of clothes URL
    """
    file ="data/WomenClothURL.txt"
    if sex == 1:
        file = "data/MenClothURL.txt"
    
    f = open(file,'r')
    queue = f.read().split()
    return queue

def get_all_prodURL(CategoryURL,filename):
    """
    Arguments:
        CategoryURL - the first page of each category
    """
    t = 5
    i = 1
    while(True):
        t -= 1
        flag = get_productURL(CategoryURL+ "&page=" + str(i),filename)
        i+=1
        if t == 0 or flag == 0:
            break;
    
        #에러가 나면 savepoint에 진행상황(카테고리, i번째 페이지, j번째 prod) 를 저장하고 종료
    
    #카테고리별로 페이지를 돈다
    return

def get_productURL(pageURL,filename):
    #한 페이지에서 각각 상품의 url을 수집해서 파일에 넣는다
    """
    Arguments:
        pageURL - URL of products list Page
        filename
    
    return:
        nothing - 0 if there's no extra product URLs else 1
    """
    nothing = 0
    response = requests.get(pageURL)
    soup = bs(response.text, 'html.parser')
    product = soup.find_all("div",{"class":PATTERN})
    
    if product:
        f = open(filename,'a')
        for i,_ in enumerate(product):
            f.write(HOME_PAGE + product[i].find("a",{"href" : re.compile("/.*")})["href"]+"\n")
        f.close()
    else:
        nothing = 1 
    
    return nothing

def get_information(prodURL,categoryURL,index):
    """
    collect data into csv file from page 
    Arguement:
        prodURL - URL of each product 
    """
    response = requests.get(prodURL)
    soup = bs(response.text,'html.parser')
    
    
    
    id = allocate_id(categoryURL,index)
    category = extract_category(categoryURL)
    name = extractName(soup)
    data = extractData(soup)
    merge = (id+ category+ name + data)
    
    saveImage(soup,id[0][1] + ".jpg")    
    
    return merge
    

def store_savepoint():
    return

def write_data(data,header,csv_writer):
    """
    data - (list of tuple) 
    header - 
    file - csv file to write 
    """
    row = [None for _ in header]
    for i in range(len(data)):
        try:
            row[header.index(data[i][0])] = data[i][1]
        except ValueError:
            header.append(data[i][0])
            row.append(data[i][1])
    
    csv_writer.writerow(row)

def main():
    global header
    header = ['id', 'category', 'name', 'Color', 'Composition', 'Style',
          'Sleeve Length', 'Neckline', 'Pattern Type', 'Fabric',
          'Season', 'Fit Type', 'Length', 'Placket Type', 'Occasion','Decoration',
          'Sleeve Type', 'Hem Shaped', 'Material', 'Arabian Clothing', 'Belt', 'Type', 'Lining',
           'Chest pad', 'Waist Type', 'Pant Type', 'Closure Type', 'Pant Length', 'Silhouette']
    
    categoryURL_F = get_categoryURL(0)
    for url in categoryURL_F:
        get_all_prodURL(url,FILENAME_F)
        pageURL = open(FILENAME_F,'r')
        prodURLs = pageURL.read().split()
        for i in range(len(prodURLs)):
            prodURL = prodURLs[i]
            f = open('female.csv','a',newline ='')
            wr = csv.writer(f)
            try:
                data = get_information(prodURL,url,i)
                write_data(data,header,wr)
                f.close()
            except:
                continue
        pageURL.close()
        clear(FILENAME_F)

    """        
    categoryURL_M = get_categoryURL(1)
    for url in categoryURL_M:
        get_all_prodURL(url, FILENAME_M)
    
    pageURL = open("prodURL_M.txt",'r')
    prodURLs = pageURL.read().split()
    """
    return

def clear(FILEAME):
    open(FILEAME, "w").close()

def saveImage(soup,filename):
    img_key = {"class" : "j-lazy-dpr-img j-change-main_image"}
    img_url = "https:" + soup.find("img",img_key)['data-src']
    urllib.request.urlretrieve(img_url, IMAGE_PATH + "\\" + filename)
    return

def extractName(soup):
    refined = soup.find("h4", {"class" : "name"}).text
    for char in MASS:
        refined = refined.replace(char,'')
    
    return [('name' , refined.strip())]

def extractData(soup):
    data_div = soup.find_all("div", {"class" : "kv-row"})
    key = {"class" : "key"}
    val = {"class" : "val"}
    row = []
    for div in data_div:
        column = div.find("div",key).text.replace(":","").strip()
        value = div.find("div",val).text.strip()
        row.append((column,value))
    return row

def allocate_id(categoryURL, index):
    key = "id"
    val = re.search(r'(?<=icn=).*(?=&ici)',categoryURL).group() + str('%04d'%index)
    return [(key , val)]


def extract_category(categoryURL):
    return [("category" , re.search(r'(?<=com/).*(?=-c)',categoryURL).group())]

main()
f = open("header.csv",'w')
header =['id',
 'category',
 'name',
 'Color',
 'Composition',
 'Style',
 'Sleeve Length',
 'Neckline',
 'Pattern Type',
 'Fabric',
 'Season',
 'Fit Type',
 'Length',
 'Placket Type',
 'Occasion',
 'Decoration',
 'Sleeve Type',
 'Hem Shaped',
 'Material',
 'Arabian Clothing',
 'Belt',
 'Type',
 'Lining',
 'Chest pad',
 'Waist Type',
 'Pant Type',
 'Closure Type',
 'Pant Length',
 'Silhouette',
 'Collar',
 'Shirt Type',
 'Suit Type',
 'Sweater Type',
 'Placket',
 'Bra Type',
 'Bottom Type',
 'Panty Type']
wr = csv.writer(f)
wr.writerow(header)
f.close()
