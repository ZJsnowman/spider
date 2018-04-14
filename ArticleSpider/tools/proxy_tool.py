__author__ = 'ZJsnowman'
# -*- coding:utf-8 -*-
import requests
import time

test_url = "https://www.tianyancha.com"
timeout = 60.0


def test_proxy(proxy):
    proxies = {
        'http': 'http://' + proxy
    }
    # try:
    start_time = time.time()
    requests.get(test_url, proxies=proxies, timeout=timeout)
    end_time = time.time()
    use_time = end_time - start_time
    print('valid proxy,userd time:' + str(use_time))
    # except Exception as e:
    #     print('invalid proxy', proxy, e)


test_proxy('115.226.148.100:33790')
