__author__ = 'ZJsnowman'
# -*- coding:utf-8 -*-
from selenium import webdriver
from scrapy import Selector
browser=webdriver.Chrome(executable_path='/Users/zhangjun/data/spider/chromedriver')
browser.get("https://detail.tmall.com/item.htm?id=44263449260&spm=875.7931836/B.2017077.6.66144265EUBCKW&scm=1007.12144.81309.73263_0&pvid=ea7cb864-5a63-47e3-94b0-1d7d15c82d7a&sm=true&smToken=2c386cfbe60c45f5ad97d838193e95c3&smSign=qGXxlUE4kUcX58xukST04g==")
# print(browser.page_source)
browser.find_element_by_xpath("")

t_selector=Selector(text=browser.page_source)
print(t_selector.xpath("//div[@class='tm-promo-price']/span/text()").extract())
# browser.quit()