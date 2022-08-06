# -*- coding:utf-8 -*-
# ※Author = 胡志达
# ※Time = 2022/8/1 22:30
# ※File Name = cosplay.py
# ※Email = 840831038@qq.com

import requests
import re
from concurrent.futures import ThreadPoolExecutor
import os
import time
from tenacity import retry, wait_fixed, stop_after_attempt

os.chdir("D://Cosplay/")

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

pic_host = 'https://t2cy.com'

htmls = []
fails = []

find_html_url = re.compile('<h3><a href="(.*?)" target="_blank" title=".*?">.*?</a></h3>')
find_title = re.compile('<title>(.*?)</title>')
find_author = re.compile('<h3 class="fb orange mt10">(.*?)</h3> ')
find_content = re.compile('<h3 class="mt20 lh150">(.*?)</h3>',re.S)
find_pic_url = re.compile('<p><img class="lazy" data-loadsrc="(.*?)" alt=".*?" />')
find_picture_url = re.compile('<p><img src="(.*?)" alt=".*?" /></p>')
find_lazy_pic_src_url = re.compile('<p><img class="lazy" alt=".*?" data-loadsrc="(.*?)" /></p>')
find_alt_src_url = re.compile('<p><img class="lazy" data="loadsrc="(.*?)".*?')
find_lazy_data_loadsrc = re.compile('<p><img alt="D.va同人兔女郎 " src="(.*?)" /></p>')

class COS:
    def __init__(self, html_url:str='', title:str='', author:str='', content:str='', pic_urls=None):
        if pic_urls is None:
            pic_urls = []
        self.html_url = html_url
        self.title = title
        self.author = author
        self.content = content
        self.pic_urls = pic_urls

def get_html_url():
    for count in range(30):
        if count == 1:
            url = 'https://t2cy.com/acg/cos/index.html'
        else:
            url = f'https://t2cy.com/acg/cos/index_{count}.html'

        req = requests.get(url = url,headers = headers)
        if req.status_code == 200:
            response = req.content.decode()
            for i in re.findall(find_html_url,response):
                if i not in htmls:
                    htmls.append(pic_host+i)

def parse_html(url):
    req = requests.get(url=url, headers=headers)
    if req.status_code != 200:
        # continue
        print(req.content.decode())
        print(f'{url} status code {req.status_code}')
        pass
    else:
        cos = COS()
        cos.html_url = url
        response = req.content.decode()
        cos.title = re.findall(find_title,response)[0]
        cos.content = re.findall(find_content,response)[0]
        cos.author = re.findall(find_author,response)[0]
        cos.pic_urls = [(pic_host+i) for i in re.findall(find_pic_url,response)]
        if len(cos.pic_urls) == 0:
            # print(response)
            cos.pic_urls = [i if i[0:4]=='http' else pic_host+i for i in re.findall(find_picture_url,response)]
            if len(cos.pic_urls)==0:
                cos.pic_urls = [pic_host+i for i in re.findall(find_lazy_pic_src_url,response)]
                if len(cos.pic_urls) == 0:
                    cos.pic_urls = [i for i in re.findall(find_alt_src_url,response)]
                    if len(cos.pic_urls)==0:
                        cos.pic_urls = [i for i in re.findall(find_lazy_data_loadsrc,response)]
        print(f'{url} -> {len(cos.pic_urls)}')
        upload(cos)
    pass

def upload(cos:COS):
    if not os.path.exists(f'./{cos.title}'):
        os.mkdir(f'./{cos.title}')
    with open(f'./{cos.title}/readme.txt','w',encoding='utf-8') as f:
        f.write(f'''{cos.title}\n{cos.pic_urls}\n{cos.content}\n{cos.html_url}\n''')

    for count in range(len(cos.pic_urls)):
        time.sleep(1)
        pic = requests.get(cos.pic_urls[count], headers=headers)
        if pic.status_code == 200:
            type = cos.pic_urls[count][cos.pic_urls[count].index('.', -6, -1) + 1:]
            with open(f'./{cos.title}/{count + 1}.{type}', 'wb') as f:
                f.write(pic.content)
        else:
            fails.append(cos.pic_urls)
    print(f'{cos.title} done!')
    time.sleep(2)

def dir_miss_process(dir):
    with open(f'./{dir}/readme.txt','r',encoding='utf-8') as f:
        x = f.readlines()
        urls = x[1]
        urls = urls.rstrip(']').lstrip('[').replace('\'','').split(',')
        # print(urls)
        url = x[-1]

        if len(os.listdir(f'./{dir}')) < len(urls)-1:
            print('yes')
            parse_html(url.replace('\n',''))
        else:
            print("no")

def delete_readme():
    dirs = os.listdir()
    for dir in dirs:
        os.remove(f'./{dir}/readme.txt')

if __name__ == '__main__':
    # get_html_url()
    # pool = ThreadPoolExecutor(16)
    # dirs = os.listdir()
    # futures = pool.map(dir_miss_process,dirs)
    delete_readme()

