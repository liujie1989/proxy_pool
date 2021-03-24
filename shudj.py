import requests
from fake_useragent import UserAgent
import time,random


ua=UserAgent()
ua.update
#http请求头
Hostreferer = {
    'User-Agent': ua.random,
    'Referer': 'https://tianma.liubeiwen.com'
               }
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml(count):
    # ....
    timeout=30
    while count>0:
        print('第',count,'次进入')
        proxy = get_proxy().get("proxy")
        retry_count = 5
        while retry_count > 0:
            try:
                html = requests.get('https://newyork.liubeixiazai.com/?fromuid=803198',timeout=timeout, proxies={"https": "http://{}".format(proxy)},headers=Hostreferer)
                # html = requests.get('https://httpbin.org/get?show_env=1', proxies={"https": "http://{}".format(proxy)},headers=Hostreferer)
                html = requests.get(html.url,timeout=timeout, proxies={"https": "http://{}".format(proxy)},headers=Hostreferer)
                # 使用代理访问
                print('第',count,'次完成')
                count -= 1
                # time.sleep(random.random()*3)
                break
            except Exception:
                print('第',count,'次',proxy,'异常')
                retry_count -= 1
        # 删除代理池中代理
        if(retry_count==0):
            print('代理',proxy,'删除')
            delete_proxy(proxy)
    return None


if __name__ == "__main__":
    count =50
    getHtml(count)

    