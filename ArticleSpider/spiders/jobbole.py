# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobJobbleArticleItem
from ArticleSpider.utils.common import get_md5
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_urls_node = response.xpath("//div[@class='post floated-thumb']/div/a")
        for node in post_urls_node:
            post_url = node.xpath('@href').extract_first()
            image_url = node.xpath('img/@src').extract_first()
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        next_url = response.xpath("//a[@class='next page-numbers']/@href").extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        article_item = JobJobbleArticleItem()

        front_image_url = response.meta.get('front_image_url', '')
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_time = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·',
                                                                                                                    '').strip()
        parise_number = response.xpath(
            "//span[@class=' btn-bluet-bigger href-style vote-post-up   register-user-only ']/h10/text()").extract_first()
        collect_number = response.xpath("//div[@class='post-adds']/span[last()]/text()").extract_first().split()[0]
        if collect_number == '收藏':
            collect_number = 0
        comment_number = \
            response.xpath("//span[@class='btn-bluet-bigger href-style hide-on-480']/text()").extract()[0].split()[0]
        if comment_number == '评论':
            comment_number = 0
        content = response.xpath("//div[@class='entry']").extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ','.join(tag_list)

        article_item['title'] = title
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['front_image_url'] = [front_image_url]
        try:
            create_time = datetime.datetime.strptime(create_time, '%Y%m%d').date()
        except Exception as e:
            create_time = datetime.datetime.now().date()
        article_item['create_time'] = create_time
        article_item['parise_number'] = parise_number
        article_item['collect_number'] = collect_number
        article_item['comment_number'] = comment_number
        article_item['content'] = content
        article_item['tags'] = tags

        yield article_item
