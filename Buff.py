# conding=utf-8
# ※Author = 胡志达
# ※Time = 2022/1/31 17:32
# ※File Name = Buff.py
# ※Email = 840831038@qq.com

import re
import json
import time
import requests
import numpy as np
from sklearn import *
import matplotlib.pyplot as plt
import sklearn
from fake_useragent import UserAgent
import pymysql

host = 'localhost'
port = 3306
db = 'buff'
user = 'root'
password = '123456'

session = requests.session()

proxies = {
    "http": None,
    "https": None,
}


class good:
    def __init__(self, id, price, market_hash_name, name, assetid, classid, goods_id, instanceid, paintwear, state):
        self.market_hash_name = market_hash_name
        self.name = name
        self.assetid = assetid
        self.classid = classid
        self.goods_id = goods_id
        self.instanceid = instanceid
        self.paintwear = paintwear
        self.state = state
        self.price = price
        self.id = id



cookies = {'_ntes_nuid': '2ff53268bcc020cfaf53b7c9e1941561',
           ' vinfo_n_f_l_n3': 'd18d1975f82800ad.1.0.1613796877231.0.1613796933717',
           ' Device-Id': 'XcjJIKl9UVMHuvmZEIs2', ' _ntes_nnid': '2ff53268bcc020cfaf53b7c9e1941561,1638168785284',
           ' Qs_lvt_382223': '1641048273', ' Qs_pv_382223': '1049491037998738200', ' _clck': 'nlt12|1|exr|0',
           ' _ga_C6TGHFPQ1H': 'GS1.1.1641048273.1.0.1641048630.0', ' _ga': 'GA1.2.941385069.1616766651',
           ' UM_distinctid': '17e2386826f140-0f51b2ce356929-4303066-144000-17e238682701032',
           ' _gid': 'GA1.2.362719380.1643813513', ' Locale-Supported': 'zh-Hans', ' game': 'csgo',
           ' NTES_YD_SESS': '09tyNtqDKRNW3HRSpM8jW9kXBw6JF9bKhBMIXhFlXmy4O1zGOBYERDkYOZddYDkEE28xQjWKn_GZrFnJaFYZKHK35KdS69wBuxVlJNyOEi18.W0ypRXsQNRNEbL7uujAv9400.FFtqlYD0IABnVWkrIQsR7jdzyI_YyEhTs3VTilOZWSjwu6lrWGnEmMPrrhKI9PDD_3.5N.PaHUNTCs.zwn9R161miAze5dYZ4b3uS2k',
           ' S_INFO': '1643878709|0|0&60##|13997965383',
           ' P_INFO': '13997965383|1643878709|1|netease_buff|00&99|hub&1643876215&netease_buff#hub&420000#10#0#0|&0|null|13997965383',
           ' remember_me': 'U1095376821|dqR1bEYBbvwE7N6k8RlqEUcEMXe5fa3j', ' _gat_gtag_UA_109989484_1': '1'}
cookiestr = "_ntes_nuid=2ff53268bcc020cfaf53b7c9e1941561; vinfo_n_f_l_n3=d18d1975f82800ad.1.0.1613796877231.0.1613796933717; Device-Id=XcjJIKl9UVMHuvmZEIs2; _ntes_nnid=2ff53268bcc020cfaf53b7c9e1941561,1638168785284; Qs_lvt_382223=1641048273; Qs_pv_382223=1049491037998738200; _clck=nlt12|1|exr|0; _ga_C6TGHFPQ1H=GS1.1.1641048273.1.0.1641048630.0; _ga=GA1.2.941385069.1616766651; UM_distinctid=17e2386826f140-0f51b2ce356929-4303066-144000-17e238682701032; _gid=GA1.2.362719380.1643813513; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=09tyNtqDKRNW3HRSpM8jW9kXBw6JF9bKhBMIXhFlXmy4O1zGOBYERDkYOZddYDkEE28xQjWKn_GZrFnJaFYZKHK35KdS69wBuxVlJNyOEi18.W0ypRXsQNRNEbL7uujAv9400.FFtqlYD0IABnVWkrIQsR7jdzyI_YyEhTs3VTilOZWSjwu6lrWGnEmMPrrhKI9PDD_3.5N.PaHUNTCs.zwn9R161miAze5dYZ4b3uS2k; S_INFO=1643878709|0|0&60##|13997965383; P_INFO=13997965383|1643878709|1|netease_buff|00&99|hub&1643876215&netease_buff#hub&420000#10#0#0|&0|null|13997965383; remember_me=U1095376821|dqR1bEYBbvwE7N6k8RlqEUcEMXe5fa3j;; _gat_gtag_UA_109989484_1=1;"

get_headers = {
    'authority': 'buff.163.com',
    'method': 'GET',
    'path': '/api/message/notification?_=1643540363231',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'cookie': cookiestr,
    'pragma': 'no-cache',
    'referer': 'https://buff.163.com/market/steam_inventory?game=csgo',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': str(UserAgent().random),
    'x-requested-with': 'XMLHttpRequest'
}

def get_connection():
    conn = pymysql.connect(host=host,port=port,db=db,user=user,password=password)
    return conn

def sell(market_hash_name, assetid, classid, instanceid, goods_id, price, state):
    if state == 3:
        sell_order = "https://buff.163.com/market/sell_order/preview/manual_plus"
        create_sell = "https://buff.163.com/api/market/sell_order/create/manual_plus"
        payload = '''{
            "game":"csgo",
            "assets":[
                {
                    "game":"csgo",
                    "market_hash_name":"%s)",
                    "contextid":2,
                    "assetid":"%s",
                    "classid":"%s",
                    "instanceid":"%s",
                    "goods_id":%d,
                    "price":"",
                    "income":"",
                    "has_market_min_price":false
                }
            ]
        }
        ''' % (market_hash_name, assetid, classid, instanceid, goods_id)
        payload = json.loads(payload)

        inventry = "https://buff.163.com/market/steam_inventory?game=csgo#page_num=1&page_size=50&search=&state=all"
        req = session.get(inventry, cookies=cookies, headers=get_headers, proxies=proxies)
        find = re.compile(r'<meta name="csrf_token" content="(.*?)">')
        csrf_token = re.findall(find, req.text)[0]

        payload["csrf_token"] = csrf_token
        token = session.cookies["csrf_token"]
        s = session.cookies["session"]
        length = str(len(payload))
        post_headers = {
            'authority': 'buff.163.com',
            'method': 'POST',
            'path': '/market/sell_order/preview/manual_plus',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-length': length,
            'content-type': 'application/json',
            'cookie': '%s session=%s; csrf_token=%s' % (
                cookiestr, s, token),
            'origin': 'https://buff.163.com',
            'pragma': 'no-cache',
            'referer': 'https://buff.163.com/market/steam_inventory?game=csgo',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'x-csrftoken': token,
            'x-requested-with': 'XMLHttpRequest'
        }
        session.post(sell_order, headers=post_headers, json=payload, proxies=proxies)

        stamp = str(time.time()).replace(".", "")[:13]
        fee_url = "https://buff.163.com/api/market/batch/fee?game=csgo&prices=%.2f&goods_ids=%d&is_change=0&check_price=1&_=%s" % (
            price, goods_id, stamp)
        req1 = session.get(fee_url, proxies=proxies, headers=get_headers)
        req1 = req1.json()
        income = price - float(req1["data"]["fees"][0])

        payload["assets"][0]["market_hash_name"] = market_hash_name
        payload["assets"][0]["contextid"] = 2
        payload["assets"][0]["assetid"] = assetid
        payload["assets"][0]["classid"] = classid
        payload["assets"][0]["instanceid"] = instanceid
        payload["assets"][0]["goods_id"] = goods_id
        payload["assets"][0]["price"] = price
        payload["assets"][0]["income"] = income
        payload["assets"][0]["cdkey_id"] = ""

        stamp = str(time.time()).replace(".", "")[:13]
        batch1 = "https://buff.163.com/api/market/batch/fee?game=csgo&prices=%f&cdkey_ids=&_=%s" % (price, stamp)
        session.get(batch1, proxies=proxies)
        # print(session.cookies["csrf_token"])
        stamp = str(time.time()).replace(".", "")[:13]
        batch2 = "https://buff.163.com/api/market/get_prices_from_incomes?game=csgo&incomes=%.2f&_=%s" % (price, stamp)
        session.get(batch2, proxies=proxies)
        # print(session.cookies["csrf_token"])
        stamp = str(time.time()).replace(".", "")[:13]
        batch3 = "https://buff.163.com/api/market/batch/fee?game=csgo&prices=%f&cdkey_ids=&_=%s" % (price, stamp)
        session.get(batch3, proxies=proxies)
        # print(session.cookies["csrf_token"])
        stamp = str(time.time()).replace(".", "")[:13]
        batch4 = "https://buff.163.com/api/market/batch/fee?game=csgo&prices=%f&goods_ids=%d&is_change=0&check_price=1&_=%s" % (
            price, goods_id, stamp)
        session.get(batch4, proxies=proxies)
        inventry = "https://buff.163.com/market/steam_inventory?game=csgo"
        req = session.get(inventry, headers=get_headers, proxies=proxies)
        csrf_token = re.findall(find, req.text)[0]
        payload["csrf_token"] = csrf_token
        token = session.cookies["csrf_token"]
        s = session.cookies["session"]
        length = str(len(payload))
        post_headers = {
            'authority': 'buff.163.com',
            'method': 'POST',
            'path': '/market/sell_order/preview/manual_plus',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-length': length,
            'content-type': 'application/json',
            'cookie': '%s session=%s; csrf_token=%s' % (
                cookiestr, s, token),
            'origin': 'https://buff.163.com',
            'pragma': 'no-cache',
            'referer': 'https://buff.163.com/market/steam_inventory?game=csgo',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'x-csrftoken': token,
            'x-requested-with': 'XMLHttpRequest'
        }

        reqs = session.post(create_sell, proxies=proxies, json=payload, headers=post_headers)
        print(reqs.text)
    elif state == 2:
        print("物品已经在售")
    else:
        print("无法出售，steam时限。")
    return

def buy_headers(payload, session):
    length = str(len(payload))
    token = session.cookies["csrf_token"]
    s = session.cookies["session"]

    post_headers = {
        'authority': 'buff.163.com',
        'method': 'POST',
        'path': '/api/market/goods/buy',
        'scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-length': length,
        'content-type': 'application/json',
        'cookie': '%s session=%s;  csrf_token=%s' % (cookiestr, s, token),
        'origin': 'https://buff.163.com',
        'pragma': 'no-cache',
        'referer': 'https://buff.163.com/goods/878864?from=market',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'x-csrftoken': token,
        'x-requested-with': 'XMLHttpRequest'
    }
    return post_headers

def buy(sell_order_id, goods_id, price):
    payload = '''{"game":"csgo","goods_id":%d,"sell_order_id":"%s","price":"%.2f","pay_method":1,"allow_tradable_cooldown":0,"token":"","cdkey_id":""}''' % (
    goods_id, sell_order_id, price)
    stamp = str(time.time()).replace(".", "")[:13]
    info = "https://buff.163.com/account/api/user/info?_=%s" % stamp
    # session = requests.session()
    session.get(info, proxies=proxies, headers=get_headers, cookies=cookies)
    stamp = str(time.time()).replace(".", "")[:13]

    preview = "https://buff.163.com/api/market/goods/buy/preview?game=csgo&sell_order_id=%s&goods_id=%d&price=%.2f&allow_tradable_cooldown=0&cdkey_id=&_=%s" % (
        sell_order_id, goods_id, price, stamp)
    session.get(preview, proxies=proxies, headers=get_headers)
    stamp = str(time.time()).replace(".", "")[:13]
    cupon = "https://buff.163.com/api/activity/coupon/my/?state=unuse&coupon_type=reduction&order_amount=%.2f&sell_order_id=%s&_=%s" % (
        price, sell_order_id, stamp)

    payload = json.loads(payload)
    refer = "https://buff.163.com/goods/%d?from=market" % goods_id
    req = session.get(refer, cookies=cookies, headers=get_headers, proxies=proxies)
    find = re.compile(r'<meta name="csrf_token" content="(.*?)">')
    csrf_token = re.findall(find, req.text)[0]
    print("cs:" + csrf_token)
    payload["csrf_token"] = csrf_token

    post_headers = buy_headers(payload, session)
    buy = "https://buff.163.com/api/market/goods/buy"
    req = session.post(buy, headers=post_headers, proxies=proxies, json=payload)
    req = req.json()
    bill_order = req["data"]["id"]

    stamp = str(time.time()).replace(".", "")[:13]
    infos = "https://buff.163.com/api/market/bill_order/batch/info?bill_orders=%s&_=%s" % (bill_order, stamp)
    session.get(infos, headers=get_headers, proxies=proxies)

    payload2 = '''{"bill_orders":["%s"],"game":"csgo"}''' % bill_order
    payload2 = json.loads(payload2)
    req = session.get(refer, headers=get_headers, proxies=proxies)
    # find = re.compile(r'<meta name="csrf_token" content="(.*?)">')
    csrf_token = re.findall(find, req.text)[0]
    print("cs:" + csrf_token)
    payload2["csrf_token"] = csrf_token
    ask_sell = "https://buff.163.com/api/market/bill_order/ask_seller_to_send_offer"
    post_headers = buy_headers(payload2, session)

    req = session.post(ask_sell, headers=post_headers, proxies=proxies, json=payload2)
    print(req.text)
    return

def load_good(req):
    goods_list = []
    items = req["data"]["items"]
    for item in items:
        goods_id = req["data"]["items"][items.index(item)]["goods_id"]
        market_hash_name = req["data"]["goods_infos"][str(goods_id)]["market_hash_name"]
        name = req["data"]["goods_infos"][str(goods_id)]["name"]
        assetid = item["asset_info"]["assetid"]
        classid = item["asset_info"]["classid"]
        instanceid = item["asset_info"]["instanceid"]
        if item["asset_info"]["paintwear"] is not None:
            paintwear = item["asset_info"]["paintwear"]
        else:
            paintwear = ""
        state = item["state"]
        if item["sell_min_price"]:
            price = item["sell_min_price"]
        else:
            price = None
        if "id" in item.keys():
            id = item["id"]
        else:
            id = ""
        goods = good(id, price, market_hash_name, name, assetid, classid, goods_id, instanceid, paintwear, state)
        goods_list.append(goods)
    return goods_list

def linear_model_main(X_parameters, Y_parameters):  # , predict_value
    regr = linear_model.LinearRegression()
    # scaler = sklearn.preprocessing.StandardScaler()
    # X_parameters = scaler.fit_transform(X_parameters)
    # Y_parameters = scaler.fit_transform(Y_parameters)
    regr.fit(X_parameters, Y_parameters)
    predict_outcome1 = regr.predict(np.array(0).reshape(-1, 1))
    predict_outcome2 = regr.predict(np.array(1).reshape(-1, 1))
    predictions = {}

    # predictions['intercept'] = regr.intercept_ #截距
    # predictions['coefficient'] = regr.coef_ #常数项
    predictions['b'] = predict_outcome1
    predictions['k'] = predict_outcome2 - predict_outcome1
    return X_parameters, Y_parameters, predictions


# noinspection SqlDialectInspection
def get_my_store_by_wanna(goods_name):
    baseurl = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id="
    stamp = str(time.time()).replace(".", "")[:13]
    url = "https://buff.163.com/api/market/steam_inventory?game=csgo&force=0&page_num=1&page_size=50&search=&state=all&_=%s" % stamp
    session = requests.session()
    req = session.get(url, headers=get_headers, proxies=proxies, cookies=cookies)
    req = req.json()
    goods = load_good(req)
    wanna = goods_name
    conn = get_connection()
    cursor = conn.cursor()
    for good in goods:
        if good.name not in wanna:
            try:
                stamp = str(time.time()).replace(".", "")[:13]
                url = "https://buff.163.com/api/market/goods/price_history/buff?game=csgo&goods_id=%d&currency=CNY&_=%s" % (
                good.goods_id, stamp)
                req = session.get(url, headers=get_headers, proxies=proxies)
                req = req.json()
                price_historys = req["data"]["price_history"]
                times = []
                prices = []
                for price_history in price_historys:
                    times.append(float(price_history[0] / 100000000))
                    prices.append(price_history[1])
                times = np.array(times[-100:]).reshape(-1, 1)
                prices = np.array(prices[-100:]).reshape(-1, 1)
                times, prices, predict = linear_model_main(times, prices)
                # show_linear_line(times,prices)
                sql = "insert into my_store (name,assetid,classid,instanceid,market_hash_name,goods_id,buy_price,price,state,paintwear,k) values('{}','{}','{}','{}','{}',{},{},{},{},'{}',{}) ON DUPLICATE KEY UPDATE name='{}',assetid='{}',classid='{}',market_hash_name='{}',goods_id={},buy_price={},price={},state={},paintwear='{}',k={}".format(good.name,good.assetid,good.classid,good.instanceid,good.market_hash_name,int(good.goods_id),0,float(good.price),int(good.state),good.paintwear,predict["k"][0][0],good.name,good.assetid,good.classid,good.market_hash_name,int(good.goods_id),0,float(good.price),int(good.state),str(good.paintwear),float(predict["k"][0][0]))
                # print(sql)
                cursor.execute(sql)
                print(good.name + ":" + str(predict["k"][0][0]))
                # if predict["k"][0][0] < 0:
                    # sell(good.market_hash_name, good.assetid, good.classid, good.instanceid, good.goods_id,float(good.price),good.state)
            except:
                 print(good.name)
    conn.commit()
    cursor.close()
    conn.close()

def show_linear_line(X_parameters, Y_parameters):
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    plt.scatter(X_parameters, Y_parameters, color='blue')
    plt.plot(X_parameters, regr.predict(X_parameters), color='red', linewidth=4)
    plt.show()

if __name__ == "__main__":
    stamp = time.time()
    get_my_store_by_wanna([])
    stamp2 = time.time()
    print(stamp2-stamp)
# ["AK-47 | 霓虹革命 (久经沙场)",
#                            "USP 消音版 | 脑洞大开 (久经沙场)",
#                            "格洛克 18 型（StatTrak™） | 城里的月光 (崭新出厂)",
#                            "M4A1 消音型（StatTrak™） | 破碎铅秋 (久经沙场)",
#                            "P90 | 大怪兽 RUSH (略有磨损) ",
#                            "AWP（StatTrak™） | 死神 (久经沙场) ",
#                            "MAG-7（StatTrak™） | SWAG-7 (略有磨损) ",
#                            ]