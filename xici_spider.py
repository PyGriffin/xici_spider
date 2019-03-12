import requests
from fake_useragent import UserAgent
from lxml import etree
import pandas as pd
import time

class XiCi(object):
    '''
    爬取西刺的代理ip（ip:prot type）
    爬取网址：
    爬取工具requests
    '''
    def __init__(self):
        self.url = 'https://www.xicidaili.com/nn/{}'
        self.ua = UserAgent()
        # self.porxy = {
        #     'http':'125.126.205.151:9999'
        # }
        self.headers = {
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTA5YjA2NTVhODMwOWNjOGE1ZmZlZjhjMjhiZGI2YjE1BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWYyMlJndlAyMFJCVkRYM1BHTW5GUGozayttWEU1MGQ0SEJ3cHJSOXdsVFk9BjsARg%3D%3D--d92253874ee66fd83cb5a03913c2a66bf24b4aec; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1551799148,1552144307,1552313837; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1552313928',
            'Host': 'www.xicidaili.com',
            'If-None-Match': 'W/"32d4ef12ff5bac74641134031ae1b166"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random,
        }

    def get_res(self,url):
        # 获取响应
        res = requests.get(url, headers=self.headers)
        return res.content.decode()

    def get_content(self,res):
        res_html = etree.HTML(res)
        print(res)
        tr_list = res_html.xpath('//table[@id="ip_list"]//tr')
        print(len(tr_list))
        proxy_list = []
        for tr in tr_list:
            item = {}
            try:
                ip = tr.xpath('./td[2]/text()')
                port = tr.xpath('./td[3]/text()')
                h_type = tr.xpath('./td[6]/text()')
                item[h_type[0]] = '{}:{}'.format(ip[0], port[0])
                print(item)
            except Exception as e:
                print('cuowu%s'%e)
                continue
            proxy_list.append(item)

        return proxy_list

    def save_proxy(self, proxy_list):
        df = pd.DataFrame(proxy_list)
        df.to_csv('proxy.csv',  mode='a', header=False)

    def run(self):
        page = 1
        while True:
            url = self.url.format(page)
            res = self.get_res(url)
            proxy_list = self.get_content(res)
            self.save_proxy(proxy_list)
            page += 1
            time.sleep(1)
            if len(proxy_list)<1:
                break


if __name__ == '__main__':
    xc = XiCi()
    xc.run()





























