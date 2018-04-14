__author__ = 'ZJsnowman'
# -*- coding:utf-8 -*-
import requests
from scrapy.selector import Selector
import MySQLdb
import MySQLdb.cursors

conn = MySQLdb.connect('127.0.0.1', 'root', 'zhangjun231', 'scrapy', charset="utf8", use_unicode=True)
cursor = conn.cursor()

headers = {
    "HOST": "www.xicidaili.com",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}


def crawl_ips():
    # 爬取西刺免费代理
    for i in range(1, 2750):
        result = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        selector = Selector(text=result.text)
        all_trs = selector.xpath("//table[@id='ip_list']//tr")
        ip_list = []
        for i in range(1, len(all_trs)):
            tr = all_trs[i]
            speed = tr.xpath("//td/div/@title").extract_first()
            if speed:
                speed = float(speed.split('秒')[0])
            all_text = tr.xpath(".//td/text()").extract()
            ip = all_text[0]
            port = all_text[1]
            type = all_text[5]
            ip_list.append((ip, port, type, speed))
        for ip_info in ip_list:
            cursor.execute(
                "insert ignore ip_proxy(ip,port,type,speed) VALUES('{0}','{1}','{2}','{3}')".format(
                    ip_info[0], ip_info[1], ip_info[2], ip_info[3]
                )
            )
            conn.commit()


class GetIp(object):
    def delete_ip(self, ip):
        delete_sql = """
        delete from tbl_xici_proxy where proxy='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def juage_ip(self, ip_info):
        # 判断 ip 是否可用
        https_url = "https://www.baidu.com"
        proxy_url = "https://" + ip_info
        try:
            proxy_dict = {
                "https": proxy_url
            }
            response = requests.get(https_url, proxies=proxy_dict)
            return True
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip_info)
            return False

        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip_info)
                return False

    def get_random_ip(self):
        random_sql = """SELECT tbl_xici_proxy.proxy
from tbl_xici_proxy
ORDER BY RAND()
LIMIT 1"""
        result = cursor.execute(random_sql)
        ip_info = cursor.fetchall()[0][0]
        jusge_result = self.juage_ip(ip_info)
        if jusge_result:
            return "https://" + ip_info
        else:
            return self.get_random_ip()


# if __name__ == '__main__':
#     a = GetIp()
#     print(a.get_random_ip())

# https_url = "https://www.baidu.com"
# try:
#     proxy_dict = {
#         "https": "https://63.150.152.151:3128"
#     }
#     response = requests.get(https_url, proxies=proxy_dict)
# except Exception as e:
#     print("invalid ip and port")
#
# else:
#     code = response.status_code
#     if code >= 200 and code < 300:
#         print("effective ip")
#     else:
#         print("invalid ip and port")