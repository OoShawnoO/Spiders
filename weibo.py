# conding=utf-8
# ※Author = 胡志达
# ※Time = 2022/3/1 15:23
# ※File Name = weibo.py
# ※Email = 840831038@qq.com

import requests
import json
import time
import pymysql

host = 'localhost'
port = 3306
db = 'buff'
user = 'root'
password = '123456'


def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


class Tweet:
    def __init__(self, text="", date="", like=0, comment=0, image_url="", video_url="", share=0):
        self.text = text
        self.date = date
        self.like = like
        self.comment = comment
        self.image_url = image_url
        self.video_url = video_url
        self.share = share


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "cookie": "SINAGLOBAL=5427523119814.253.1645693796782; UOR=,,www.baidu.com; wb_view_log=1536*8641.25; ULV=1646125217560:3:2:2:2092064887277.3518.1646125217499:1646119179411; wb_view_log_6650938846=1536*8641.25; webim_unReadCount=%7B%22time%22%3A1646126179375%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A62%2C%22msgbox%22%3A0%7D; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW.bzwKxC.SOBlhCv49N5Hw5JpX5KMhUgL.FoqcSK54e0nRShq2dJLoI7.RqJLXSozRehnt; ALF=1677663161; SSOLoginState=1646127166; SCF=AjGxTi9-ZDpJQuAc2-G5JBNQzEtgnQRdcr45a-DpNEnREdPHpLexLQGvC2wakQtXYjRFoTjsLGdls-nCsOStDxs.; SUB=_2A25PGZhqDeThGeBI7lIY8ybEzzqIHXVsbo6irDV8PUNbmtAKLVr3kW9NRpCc_nKH8BnPWLTx003S91gfp8Mrmnlu; XSRF-TOKEN=FHOaCWGP-695XsT2UQd76Hy-; WBPSESS=T-lY9gmAzdma7eh5vpC3BCsqQuSQB4BiAB6hxWwVq0Qe2fX7GI9HSrfjANgUVE1mXmAe-5nhWgiQPFX3QJcM4bbuC38AIVBcmzNj_wCDmysFMWptCXAE9TyCxZyFMSlVpYQP_fOPPmvlbHY0x_Odrw=="
}

proxies = {
    "http": None,
    "https": None,
}

date_list = [
    "01月03日", "01月25日", "02月16日", "03月31日", "04月08日", "05月14日", "06月26日", "07月12日", "08月17日", "09月08日", "10月07日",
    "11月12日", "12月04日", "12月26日",
]

count = 0

page = 1
displayYear = "2021"
curMonth = 1
root_url = "https://weibo.com/ajax/statuses/mymblog?uid=2803301701&page=%d&feature=0&displayYear=%s&curMonth=%s&stat_date=%s" % (
page, displayYear, curMonth, displayYear + str(curMonth))

root_urls = []

req = requests.get(root_url, headers=headers, proxies=proxies)
if req.content:
    req = req.json()

for curMonth in range(1, 13):
    if curMonth < 10:
        Month = "0" + str(curMonth)
    else:
        Month = str(curMonth)

    page = 1

    time.sleep(10)

    root_url = "https://weibo.com/ajax/statuses/mymblog?uid=2803301701&page=%d&feature=0&displayYear=%s&curMonth=%s&stat_date=%s" % (
        page, displayYear, curMonth, displayYear + Month)
    try:
        req = requests.get(root_url, headers=headers, proxies=proxies)
        req = req.json()
    except:
        root_urls.append(root_url)

    while len(req["data"]["list"]) != 0:
        root_url = "https://weibo.com/ajax/statuses/mymblog?uid=2803301701&page=%d&feature=0&displayYear=%s&curMonth=%s&stat_date=%s" % (
            page, displayYear, curMonth, displayYear + Month)
        try:
            req = requests.get(root_url, headers=headers, proxies=proxies)
            req = req.json()
        except:
            root_urls.append(root_url)

        i = 0

        while i < len(req["data"]["list"]):
            date = req["data"]["list"][i]["created_at"]
            timestamp = time.mktime(time.strptime(date, "%a %b %d %H:%M:%S %z %Y"))
            timeArray = time.localtime(timestamp)
            judge_date = time.strftime("%m月%d日", timeArray)
            print(judge_date)
            if judge_date in date_list:
                tweet = Tweet()
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)  # 2022-03-01 15:22:40
                text = req["data"]["list"][i]["text_raw"]
                try:
                    video_url = req["data"]["list"][i]["page_info"]["media_info"]["mp4_720p_mp4"]
                except:
                    video_url = ""
                like = req["data"]["list"][i]["attitudes_count"]
                comment = req["data"]["list"][i]["comments_count"]
                share = req["data"]["list"][i]["reposts_count"]
                try:
                    image_id = req["data"]["list"][i]["pic_ids"][0]
                    image_url = req["data"]["list"][i]["pic_infos"][image_id]["largest"]["url"]
                except:
                    image_url = ""
                tweet.image_url = image_url
                tweet.share = share
                tweet.like = like
                tweet.text = text
                tweet.video_url = video_url
                tweet.comment = comment
                tweet.date = otherStyleTime
                conn = get_connection()
                sql = "insert into weibo (text,likes,share,comment,image_url,video_url,date) values('{}',{},{},{},'{}','{}','{}')".format(
                    tweet.text, tweet.like, tweet.share, tweet.comment, tweet.image_url, tweet.video_url, tweet.date)
                print(sql)
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                count += 1
            i += 1
        page += 1

print(count)  #总数
print(root_urls)  #请求失败