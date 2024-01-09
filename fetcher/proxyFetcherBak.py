# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcherBak
   Description :   原文件改为自动加载爬虫程序,所以调试中或者失效的程序也会加载,
                    把调试中的程序,或者失效程序,放到这个文件里面.
   Author :        wingser
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcherBak
-------------------------------------------------
"""
__author__ = 'JHao'

import json
import re
from time import sleep

from util.webRequest import WebRequest
from pyquery import PyQuery as pq


class ProxyFetcherBak(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy04():
        """ FreeProxyList https://www.freeproxylists.net/zh/ """
        url = "https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50"
        tree = WebRequest().get(url, verify=False).tree
        from urllib import parse

        def parse_ip(input_str):
            html_str = parse.unquote(input_str)
            ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', html_str)
            return ips[0] if ips else None

        for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
            ip = parse_ip("".join(tr.xpath('./td[1]/script/text()')).strip())
            port = "".join(tr.xpath('./td[2]/text()')).strip()
            if ip:
                yield "%s:%s" % (ip, port)



    @staticmethod
    def freeProxy09(page_count=1):
        """ 免费代理库 """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url, verify=False).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()


    @staticmethod
    def wingser01():
        """
        seo方法 crawler, https://proxy.seofangfa.com/
        """
        url = 'https://proxy.seofangfa.com/'
        html_tree = WebRequest().get(url, verify=False).tree
        for index, tr in enumerate(html_tree.xpath("//table//tr")):
            if index == 0:
                continue
            yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def wingser02():
        """
        小舒代理 crawler, http://www.xsdaili.cn/
        """
        url = 'http://www.xsdaili.cn/'
        base_url = "http://www.xsdaili.cn/dayProxy/ip/{page}.html"

        '''通过网站,获取最近10个日期的共享'''
        urls = []
        html = WebRequest().get(url, verify=False).tree
        doc = pq(html)
        title = doc(".title:eq(0) a").items()
        latest_page = 0
        for t in title:
            res = re.search(r"/(\d+)\.html", t.attr("href"))
            latest_page = int(res.group(1)) if res else 0
        if latest_page:
            urls = [base_url.format(page=page) for page in range(latest_page - 10, latest_page)]
        else:
            urls = []

        '''每个日期的网站,爬proxy'''
        for u in urls:
            h = WebRequest().get(u, verify=False).tree
            doc = pq(h)
            contents = doc('.cont').text()
            contents = contents.split("\n")
            for content in contents:
                yield content[:content.find("@")]



    @staticmethod
    def wingser03():
        """
        PzzQz https://pzzqz.com/
        """
        from requests import Session
        from lxml import etree
        session = Session()
        try:
            index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
            x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
            if x_csrf_token:
                data = {"http": "on", "ping": "3000", "country": "cn", "ports": ""}
                proxy_resp = session.post("https://pzzqz.com/", verify=False,
                                          headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
                tree = etree.HTML(proxy_resp["proxy_html"])
                for tr in tree.xpath("//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()"))
                    port = "".join(tr.xpath("./td[2]/text()"))
                    yield "%s:%s" % (ip, port)
        except Exception as e:
            print(e)



    @staticmethod
    def wingser04():
        """
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
        request = WebRequest()
        import base64
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    @staticmethod
    def freeProxy06():
        """ FateZero http://proxylist.fatezero.org/ """
        url = "http://proxylist.fatezero.org/proxy.list"
        try:
            resp_text = WebRequest().get(url).text
            for each in resp_text.split("\n"):
                json_info = json.loads(each)
                if json_info.get("country") == "CN":
                    yield "%s:%s" % (json_info.get("host", ""), json_info.get("port", ""))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    p = ProxyFetcherBak()
    for _ in p.freeProxy09():
        print(_)




# http://nntime.com/proxy-list-01.htm

