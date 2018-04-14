# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from ArticleSpider.utils import common
from ArticleSpider.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobJobbleArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    image_path = scrapy.Field()
    create_time = scrapy.Field()
    parise_number = scrapy.Field()
    collect_number = scrapy.Field()
    comment_number = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                           insert into tbl_article(create_time,title, url, url_object_id,front_image_url,parise_number,collect_number,comment_number,content, tags)
                           VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s)
                           ON DUPLICATE KEY UPDATE parise_number=VALUES(parise_number), collect_number=VALUES(collect_number),comment_number=VALUES(comment_number)
                       """

        params = (self["create_time"], self["title"], self["url"], self["url_object_id"],
                  self["front_image_url"], self["parise_number"], self["collect_number"], self["comment_number"],
                  self["content"], self["tags"])

        return insert_sql, params


class CompanyAttribute(scrapy.Item):
    register_number = scrapy.Field()  # 工商注册号
    organization_code = scrapy.Field()  # 组织结构代码
    uniform_credit_code = scrapy.Field()  # 统一信用代码
    company_type = scrapy.Field()  # 公司类型
    taxpayer_identification_number = scrapy.Field()  # 纳税人识别号
    industry = scrapy.Field()  # 行业
    business_term = scrapy.Field()  # 营业期限
    approved_by_the_deadline = scrapy.Field()  # 核准日期
    registration_authority = scrapy.Field()  # 登记机关
    registered_address = scrapy.Field()  # 注册地址
    scope_of_business = scrapy.Field()  # 经营范围
    score = scrapy.Field()  # 企查查评分


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
                   insert into tbl_zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num,
                     watch_user_num, click_num, crawl_time
                     )
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
                     watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
               """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = common.extract_num("".join(self["answer_num"]))
        comments_num = common.extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topics, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time)
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
                   insert into tbl_zhihu_answer(zhihu_id, url, question_id, author_id, content, parise_num, comments_num,
                     create_time, update_time, crawl_time
                     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                     ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
                     update_time=VALUES(update_time)
               """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["parise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params
