from bs4 import BeautifulSoup
import io
import requests
import time
import random
import re
total=[17981,17134,17114,17302,16596,
       15970,15131,15177,14954,14555,
       14226,13848,13673,13122,12483,
       11245,11344,10372,9786,9254,
       8840,7843,7608,7019,6239,
       5314,3917,2688,1910,1226,
       613,121]
#total由spider_total得到

year=["23","22","21","20","19","18","17","16","15","14",
      "13","12","11","10","09","08","07","06","05","04",
      "03","02","01","00","99","98","97","96","95","94",
      "93","92"]

# user_agent = [
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
#     "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
#     "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
#     "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
#     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
#     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
# ]

def spider_total(year):
    s = requests.session()
    s.keep_alive =False
    addr='https://arxiv.org/list?archive=astro-ph&year={0}&month=all&submit=Go'.format(year)
    #headers={"user-agent":random.choice(user_agent)}
    #成功的那一次没有用headers
    response=requests.get(addr)
    response.encoding='utf-8'
    soup=BeautifulSoup(response.text,'html.parser')
    goal=soup.find(string=re.compile('total'))
    parts=goal.split(' ')
    print(parts[3])
    total.append(int(parts[3]))

def spider_pdf(year,start):
    s = requests.session()
    s.keep_alive =False
    addr1 = 'https://arxiv.org/list/astro-ph/{0}?skip={1}&show=100'.format(year,start*100)            
    #headers = {"user-agent":random.choice(user_agent)}
    response1 = requests.get(addr1)
    print("1",response1)
    response1.encoding='utf-8'
    soups=BeautifulSoup(response1.text,'html.parser')
    article_info=soups.find_all('span',class_='list-identifier')
    #article_info=soups.find_all(string=re.compile("Download PDF"))
    #print(article_info)
    article_info_len =len(article_info)
    #print(article_info_len)
    id=[]
    for k in range(article_info_len):
        a_href=article_info[k].find_all('a')
        id.append(a_href[1])
    for k in range(article_info_len):
        parts=str(id[k]).split('"')
        print(parts[1])
        addr2 = 'https://arxiv.org{0}'.format(parts[1])
        response2 = requests.get(addr2)
        print("2",response2)
        pdf_content=io.BytesIO(response2.content)
        with open('./pdf/{0}.{1}.pdf'.format(year,start*100+k+1),'wb') as file:
            file.write(pdf_content.read())
        #time.sleep(10)
    #time.sleep(60)

#for i in range(32):
#    spider_total(year[i])
        
# for i in range(32):
#     spider_pdf(year[i],i)

#spider_pdf(year[0],1)
spider_pdf(year[0],2)

