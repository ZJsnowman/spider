# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.shell import inspect_response
from ArticleSpider.items import CompanyAttribute
from ArticleSpider.tools import read_data
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from ArticleSpider import settings


class TianyanchaSpider(scrapy.Spider):
    name = 'tianyancha'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['https://www.tianyancha.com/']

    headers = {
        "HOST": "www.tianyancha.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0"
    }

    # 自定义 settings 和系统 setting 相比,这里优先级会高,会覆盖
    custom_settings = {
        "COOKIES_ENABLED": True,
    }

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=settings.CHROMEDRIVE_PATH)
        self.cookies = []
        super(TianyanchaSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self, spider):
        # 设置信号量,当爬虫退出的时候关闭 browser
        print("spider closed")
        self.browser.quit()

    def parse(self, response):
        company_list = read_data.get_company_list()
        for i, company_name in enumerate(company_list):
            search_url = 'https://www.tianyancha.com/search?key=' + company_name
            yield Request(url=search_url, callback=self.parse_result, headers=self.headers, cookies=self.cookies)

    def parse_result(self, response):
        # inspect_response(response, self)
        result_ulr = response.xpath(
            "//div[@class='b-c-white search_result_container']/div[1]//a[@class='query_name sv-search-company f18 in-block vertical-middle']/@href").extract_first()

        print(result_ulr)
        yield Request(url=result_ulr, callback=self.parse_detail, headers=self.headers)

    def parse_detail(self, response):
        # inspect_response(response, self)
        company_item = CompanyAttribute()

        register_number = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[1]/td[2]/text()").extract_first()
        organization_code = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[1]/td[4]/text()").extract_first()
        score = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[1]/td[last()]/img/@alt").extract_first()
        uniform_credit_code = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[2]/td[2]/text()").extract_first()
        company_type = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[2]/td[last()]/text()").extract_first()
        taxpayer_identification_number = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[3]/td[2]/text()").extract_first()
        industry = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[3]/td[last()]/text()").extract_first()
        business_term = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[4]/td[2]/span/text()").extract_first()
        approved_by_the_deadline = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[4]/td[last()]/text/text()").extract_first()
        registration_authority = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[5]/td[2]/text()").extract_first()
        registered_address = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[last()-1]/td[last()]/text()").extract_first()
        scope_of_business = response.xpath(
            "//table[@class='table companyInfo-table f14']//tr[last()]//span[@class='js-full-container ']/text()").extract_first()

        company_item['register_number'] = register_number
        company_item['organization_code'] = organization_code
        company_item['score'] = score
        company_item['uniform_credit_code'] = uniform_credit_code
        company_item['company_type'] = company_type
        company_item['taxpayer_identification_number'] = taxpayer_identification_number
        company_item['industry'] = industry
        company_item['business_term'] = business_term
        company_item['approved_by_the_deadline'] = approved_by_the_deadline
        company_item['registration_authority'] = registration_authority
        company_item['registered_address'] = registered_address
        company_item['scope_of_business'] = scope_of_business

        yield company_item

    def start_requests(self):
        self.cookies = self.login()

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=self.cookies, headers=self.headers)]

    def login(self):
        self.browser.get("https://www.tianyancha.com/login")
        self.browser.find_element_by_xpath(
            "//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']//input[@class='_input input_nor contactphone']").send_keys(
            "18025483634")
        self.browser.find_element_by_xpath(
            "//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']//input[@class='_input input_nor contactword']").send_keys(
            "zhangjun231")
        self.browser.find_element_by_xpath(
            "//div[@onclick='loginByPhone(event);']").click()
        import time
        time.sleep(5)
        Cookies = self.browser.get_cookies()
        # print(Cookies)
        # cookies_list = []
        # import pickle
        # for cookie in Cookies:
        #     # 写入文件
        #     f = open('/Users/zhangjun/data/spider/ArticleSpider/cookies/tianyancha/' + cookie['name'] + '.tianyancha',
        #              'wb')
        #     pickle.dump(cookie, f)
        #     f.close()
        #     cookies_list.append({cookie['name']: cookie['value']})
        return Cookies
