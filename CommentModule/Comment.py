import requests as rq
import math
import pymysql
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin,urlsplit
import json

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
	res = rq.get(url, headers = header)
	soup = BeautifulSoup(res.content, 'lxml')

	try:
		content_text = soup.select('p')[0].text
		one = content_text.find('(') + 1
		two = content_text.find(');')
		content = json.loads(content_text[one:two])
		# comment_list = content['result']['commentList']
		#
		# for i in comment_list:
		# 	print(i['contents'])
	except:
		pass
	return content

def getAllComment(turl):
	temp=getComment(turl,pageSize=1,page=1)
	num_page=math.ceil(temp['result']['pageModel']['totalRows']/100)

	comment_json_list = []
	for i in range(1,num_page+1):
		print(i)
		comment_json_list.append(getComment(turl,100,i))
	print(comment_json_list)


url = "http://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1063803&iid=26012388&oid=437&aid=0000154091&ptype=052"
# getComment(url)
getAllComment(url)
