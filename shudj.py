import random
import time

import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading


ua = UserAgent()
ua.update
# http请求头
Hostreferer = {
    'User-Agent': ua.random,
    'Referer': 'https://new12-22.book.meiguolvka.com/'
}
play86Hostreferer = {
    'User-Agent': ua.random,
    'Referer': 'http://www.play86.vip/'
}
jietiandiHostreferer = {
    'User-Agent': ua.random,
    'Referer': 'https://www.jietiandi.net/'
}

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# your spider code

def getHtml(count, url, hostRefer):
    # ....
    timeout = 30
    while count > 0:
        print('第', count, '次进入')
        proxy = get_proxy().get("proxy")
        retry_count = 5
        while retry_count > 0:
            try:

                html = requests.get(url, timeout=timeout, proxies={"https": "http://{}".format(proxy)},
                                    headers=hostRefer)
                # html = requests.get('https://httpbin.org/get?show_env=1', proxies={"https": "http://{}".format(proxy)},headers=Hostreferer)
                # html = requests.get(html.url,timeout=timeout, proxies={"https": "http://{}".format(proxy)},headers=hostRefer)
                # 使用代理访问
                print('第', count, '次完成')
                count -= 1
                time.sleep(random.random() * 3)
                break
            except Exception:
                print('第', count, '次', proxy, '异常')
                retry_count -= 1
        # 删除代理池中代理
        if (retry_count == 0):
            print('代理', proxy, '删除')
            delete_proxy(proxy)
    return None


def getEHtml(count, url, hostRefer):
    # ....
    timeout = 30
    while count > 0:
        print('第', count, '次进入')
        proxy = get_proxy().get("proxy")
        retry_count = 5
        while retry_count > 0:
            try:

                chrome_options = Options()
                chrome_options.add_argument('headless')
                chrome_options.add_argument('--proxy-server={0}'.format(proxy))
                # 一定要注意，=两边不能有空格，不能是这样--proxy-server = 202.20.16.82:10152
                browser = webdriver.Chrome(options=chrome_options)
                # browser.get('http://httpbin.org/ip')
                # print(browser.page_source)
                browser.get(url)
                time.sleep(100)
                # 使用代理访问
                print('第', count, '次完成')
                count -= 1
                browser.quit();
                time.sleep(random.random()*3)
                break
            except Exception as e:
                # print(str(e))
                print('第', count, '次', proxy, '异常')
                retry_count -= 1
        # 删除代理池中代理
        if (retry_count == 0):
            print('代理', proxy, '删除')
            delete_proxy(proxy)
    return None


def threadClick(count, url, hostRefer):
    # 创建10个线程对象
    threads = []
    for _ in range(5):
        t = threading.Thread(target=threadGetEHtml,args=(count, url, hostRefer), name="Thread-{}".format(_+1))
        threads.append(t)
        
    # 开始所有线程
    for t in threads:
        t.start()
    
    # 等待所有线程结束
    for t in threads:
        t.join()



def  threadGetEHtml(count, url, hostRefer):
    # ....
    timeout = 30
    while count > 0:
        print("Thread {}: 第 {} 次进入".format(threading.current_thread().name, count))

        proxy = get_proxy().get("proxy")
        retry_count = 5
        while retry_count > 0:
            try:

                chrome_options = Options()
                chrome_options.add_argument('headless')
                chrome_options.add_argument('--proxy-server={0}'.format(proxy))
                # 一定要注意，=两边不能有空格，不能是这样--proxy-server = 202.20.16.82:10152
                browser = webdriver.Chrome(options=chrome_options)
                # browser.get('http://httpbin.org/ip')
                # print(browser.page_source)
                browser.get(url)
                time.sleep(100)
                # 使用代理访问
                print("Thread {}: 第 {} 次完成".format(threading.current_thread().name, count))
                count -= 1
                browser.quit();
                time.sleep(random.random()*3)
                break
            except Exception as e:
                # print(str(e))
                print("Thread {}: 第 {} 次 {} 异常".format(threading.current_thread().name, count,proxy))
                retry_count -= 1
        # 删除代理池中代理
        if (retry_count == 0):
            print('代理', proxy, '删除')
            delete_proxy(proxy)
    return None

if __name__ == "__main__":
    playcount = 50
    count = 10000
    playurl = 'http://www.play86.com/u.asp?id=188517'
    url = 'https://new12-22.book.meiguolvka.com/?fromuid=803198'
    # getHtml(count,url,Hostreferer)
    eurl = 'https://www.guyunsq.com/?fromuid=6265'
    eurl = 'https://www.58shuyou.com/?fromuid=1155311'
    eurl = 'https://snyhxk.top/79279Wte'
    # getHtml(count, eurl, Hostreferer)

   # getEHtml(count,eurl,Hostreferer)
    #多线程执行
    threadClick(count,eurl,Hostreferer)

    # jietiandiurl = 'https://www.jietiandi.net/?fromuid=60642'
    # getEHtml(playcount, jietiandiurl, jietiandiHostreferer)
