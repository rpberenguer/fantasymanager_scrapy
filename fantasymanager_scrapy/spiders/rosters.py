# -*- coding: utf-8 -*-
import scrapy


class RostersSpider(scrapy.Spider):
    name = 'rosters'
    allowed_domains = ['http://espn.go.com']
    start_urls = ['http://http://espn.go.com/nba/teams/']

    def parse(self, response):
        pass
