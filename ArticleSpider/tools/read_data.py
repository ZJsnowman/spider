__author__ = 'ZJsnowman'
# -*- coding:utf-8 -*-
import pandas as pd
from ArticleSpider import settings


def get_company_list():
    df = pd.read_csv(settings.COMPANY_LIST_PATH)
    print(df['MCHT_NM'].tolist())
    return df['MCHT_NM'].tolist()


if __name__ == '__main__':
    get_company_list()
