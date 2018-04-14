__author__ = 'ZJsnowman'
# -*- coding:utf-8 -*-
import pandas as pd

## 转一下格式, json-->excel
df = pd.read_json('/Users/zhangjun/data/spider/ArticleSpider/company1.json', lines=True)
print(df.head())

writer = pd.ExcelWriter('/Users/zhangjun/data/spider/ArticleSpider/output/output.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()
