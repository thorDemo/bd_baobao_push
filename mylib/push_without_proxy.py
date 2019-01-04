from tools.push_tools import PushTool
import requests
import traceback
from threadpool import makeRequests, ThreadPool
from urllib import parse

success_count = 0
failure_count = 0
cookie = PushTool.get_cookies()


def push_url_one(domain):
    while True:
        global success_count
        global failure_count
        referer = PushTool.get_url(domain)
        r = PushTool.get_url(domain)
        headers = {
            'User-Agent': PushTool.user_agent(),
            'Referer': referer,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'api.share.baidu.com',
        }

        conn = requests.Session()
        conn.headers = headers
        # print(headers)
        # 将cookiesJar赋值给会话
        cookiesJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
        conn.cookies = cookiesJar
        payload = {'r': r, 'l': referer}
        code = 404
        url = ''
        try:
            # res = conn.get('http://api.share.baidu.com/s.gif', params=payload, timeout=10, proxies=proxies)
            res = conn.get('http://api.share.baidu.com/s.gif', params=payload, timeout=1)
            code = res.status_code
            if code == 200:
                success_count += 1
            else:
                failure_count += 1
            url = parse.unquote(res.url)
        except:
            # traceback.print_exc()
            failure_count += 1
        print('----------------------')
        print(code, url)
        print('success:%d  failure:%d' % (success_count, failure_count))


def push_url_two(domain):
    while True:
        global success_count
        global failure_count
        referer = PushTool.rand_all(domain)
        r = PushTool.rand_all(domain)
        # referer = 'http://www.zzqq.com/lsjxxx/20181010xxxxx.html'
        # r = 'http://www.baidu.com/xxxx.html'
        headers = {
            'User-Agent': PushTool.user_agent(),
            'Referer': referer,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'api.share.baidu.com',
        }

        conn = requests.Session()
        conn.headers = headers
        # print(headers)
        # 将cookiesJar赋值给会话
        cookiesJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
        conn.cookies = cookiesJar
        payload = {'r': r, 'l': referer}
        code = 404
        url = ''
        try:
            res = conn.get('http://api.share.baidu.com/s.gif', params=payload, timeout=10)
            code = res.status_code
            url = parse.unquote(res.url)
            if code == 200:
                if url == 'http://www.baidu.com/search/error.html':
                    failure_count += 1
                else:
                    success_count += 1
            else:
                failure_count += 1
        except:
            traceback.print_exc()
            failure_count += 1
        print('----------------------')
        print(code, url)
        print('success:%d  failure:%d' % (success_count, failure_count))
