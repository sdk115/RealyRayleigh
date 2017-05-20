import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import webtoon_config as WC
import json
	link = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=view_politics&pool=cbox5&lang=ko&country=KR&objectId=news437%2C0000154091&categoryId=&pageSize=10&indexSize=10&groupId=&page=1&initialize=true&useAltSort=true&replyPageSize=30&moveTo=&sort=favorite"
    while True:
        comment_url = make_link(u, page_count)
        header = {
            "Host": "apis.naver.com",
            "Referer": "http://comic.naver.com/comment/comment.nhn?titleId=" + titleId + "&no=" + no,
            "Content-Type": "application/javascript"
        }

        res = rq.get(comment_url, headers = header)
        soup = BeautifulSoup(res.content, 'lxml')
        try:
            content_text = soup.select('p')[0].text
            one = content_text.find('(') + 1
            two = content_text.find(');')
            content = json.loads(content_text[one:two])

            comments = content['result']['commentList']

            print(titleId, no)

            for comment in comments:
                print(comment['contents'])

            if not len(comments):
                break
            else:
                page_count += 1
        except:
            pass


if __name__ == "__main__":
    webtoons = get_daylywebtoons()
    for webtoon in webtoons:
        target_webtoons = get_all_webtoon(webtoon, False)
        for webtoon_page in target_webtoons:
            res = rq.get(webtoon_page)
            webtoon_page_soup = BeautifulSoup(res.content, 'lxml')
            data_parse(webtoon_page_soup, webtoon_page)
