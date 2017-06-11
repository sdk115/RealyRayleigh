import requests as rq
import math
import pymysql
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin,urlsplit, urlencode, quote, unquote
import json
import makeDict as d

def getParams(url):
# url = "http://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1063803&iid=2276852&oid=055&aid=0000529993&ptype=052"
    parsed = urlsplit(url)
    params = parse_qs(parsed.query)
    # print(params)
    return params

def getComment(turl, pageSize = 10, page = 1):
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
    try:
        res = rq.get(url, headers = header)
        soup = BeautifulSoup(res.content, 'lxml')

        content_text = soup.select('p')[0].text
        one = content_text.find('(') + 1
        two = content_text.find(');')
        content = json.loads(content_text[one:two])

    except:
        pass

    return content

def getAllComment(key_idx, turl, size=30):
    temp=getComment(turl,pageSize=1,page=1)
    num_page=math.ceil(temp['result']['pageModel']['totalRows']/size)

    data = []
    for i in range(1,num_page+1):
        # print(i)
        content = getComment(turl,size,i)
        comment_list = content['result']['commentList']

        for j in range(len(comment_list)):
            comment = comment_list[j]['contents']
            commentNo = comment_list[j]['commentNo']
            reg_time = comment_list[j]['regTime'][:19].replace("T", " ")
            userName = comment_list[j]['userName']

            # print(key_id, commentNo, comment, reg_time, userName)
            data.append([key_idx, None, commentNo, comment, reg_time, userName])
    return data

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

def insert(data):
    print(data)
    conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8mb4')
    curs = conn.cursor()
    sql = "INSERT IGNORE INTO news_comment(keyword_id, category_id, comment_no, contents, reg_time, user_name) VALUES(%s, %s, %s, %s, %s, %s)"
    try:
        curs.executemany(sql, data)
    except pymysql.IntegrityError:
        pass

    conn.commit()
    conn.close()

url = "http://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1063803&iid=26012388&oid=437&aid=0000154091&ptype=052"

#getAllComment(url)
#print(quote("문재인".encode('utf-8')))
#print()

#MySQL Connection 연결
conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8mb4')
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

# SQL문 실행
sql = "select * from news_keyword"
curs.execute(sql)

# 데이타 Fetch
keyword_list = curs.fetchall()
print(keyword_list)

sql = "select * from news_comment"
curs.execute(sql)

comment_list = curs.fetchall()
print(comment_list)

# Connection 닫기
conn.close()

Dict = d.loadDict()

for x in keyword_list:
    keyword = x[1]
    keyword_idx = x[0]
    if keyword_idx == 1 or keyword_idx == 2 or keyword_idx == 3 or keyword_idx == 4 or keyword_idx == 6:
        continue
    print(keyword_idx, keyword)
    Links = getLinks(quote(keyword.encode('euc-kr')), 1)
    for i in range(len(Links)):
        comments = getAllComment(keyword_idx, Links[i], 30)
        if comments:
            SVMData = d.makeSVMData(comments, Dict, keyword_list)
            print(SVMData)
            d.svmData2dat(SVMData, False)
            d.classify("forClassify", keyword_idx)
            classes = d.loadClassify("forClassify.classify")
            print(len(classes), classes)

            for j in range(len(comments)):
                comments[j][1] = classes[j]
            print(len(comments), comments)

            insert(tuple([tuple(x) for x in comments]))

#getComment(1, "http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=032&aid=0002794373", 50)