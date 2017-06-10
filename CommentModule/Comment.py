import requests as rq
import math
import pymysql
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin,urlsplit, urlencode, quote, unquote
import json

def getParams(url):
# url = "http://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1063803&iid=2276852&oid=055&aid=0000529993&ptype=052"
    parsed = urlsplit(url)
    params = parse_qs(parsed.query)
    # print(params)
    return params

def getComment(key_id, turl, pageSize = 10, page = 1):
    sort = 'new'
    params = getParams(turl)
    oid = params['oid'][0]
    aid = params['aid'][0]
    url = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=view_politics&pool=cbox5&lang=ko&country=KR&objectId=news"+oid+"%2C"+ aid+ "&categoryId=&pageSize="+str(pageSize)+"&indexSize=10&groupId=&page="+ str(page)+ "&initialize=true&useAltSort=true&replyPageSize=30&moveTo=&sort="+sort

    header = {
        "Host": "apis.naver.com",
        "Referer":  turl,
        "Content-Type": "application/javascript"
    }
    res = rq.get(url, headers = header)
    soup = BeautifulSoup(res.content, 'lxml')

    try:
        content_text = soup.select('p')[0].text
        one = content_text.find('(') + 1
        two = content_text.find(');')
        content = json.loads(content_text[one:two])
        comment_list = content['result']['commentList']
        data = []


        for i in range(len(comment_list)):
            comment = comment_list[i]['contents']
            commentNo = comment_list[i]['commentNo']
            reg_time = comment_list[i]['regTime'][:19].replace("T", " ")
            userName = comment_list[i]['userName']

            #print(key_id, commentNo, comment, reg_time, userName)
            data.append(tuple([key_id, None, commentNo, comment, reg_time, userName]))
        data2 = tuple(data)
        print(data)
        print(data2)
        conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8')
        curs = conn.cursor()
        sql = "INSERT INTO news_comment(keyword_id, category_id, comment_no, contents, reg_time, user_name) VALUES(%s, %s, %s, %s, %s, %s)"
        curs.executemany(sql, data2)
        conn.commit()
        conn.close()

    except:
        pass
    return content

def getAllComment(key_id, turl, size=30):
    temp=getComment(key_id, turl,pageSize=1,page=1)
    num_page=math.ceil(temp['result']['pageModel']['totalRows']/size)

    comment_json_list = []
    for i in range(1,num_page+1):
        # print(i)
        comment_json_list.append(getComment(key_id, turl,size,i))
    return (comment_json_list)

def getLinks(keyword, page=1):
    url = "http://news.naver.com/main/search/search.nhn?query="+keyword+"&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=title.basic&ic=all&so=rel.dsc&rcsection=exist:100&detail=0&pd=1&r_cluster2_start=1&r_cluster2_display=10&start=1&display=10&page="+str(page)
    html = rq.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    # print(soup)
    for tag in soup.find(id="search_div").find_all('a'):
        if tag.get('href') != None and tag.get('href').startswith('http://news.naver.com'):
            links.append(tag.get('href'))

    return links

url = "http://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1063803&iid=26012388&oid=437&aid=0000154091&ptype=052"

#getAllComment(url)
#print(quote("문재인".encode('utf-8')))
#print()

#MySQL Connection 연결
conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8')
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

# SQL문 실행
sql = "select * from news_keyword"
curs.execute(sql)

# 데이타 Fetch
rows = curs.fetchall()
print(rows)

# Connection 닫기
conn.close()

for x in rows:
    key = x[1]
    key_id = x[0]
    print(key_id, key)
    Links = getLinks(quote(key.encode('euc-kr')))
    for i in range(len(Links)):
        asdf = getAllComment(key_id, Links[i], 30)