# -*- coding: utf-8 -*-
import scrapy


class RostersSpider(scrapy.Spider):
    name = 'rosters'
    allowed_domains = ['http://espn.go.com']
    start_urls = ['http://http://espn.go.com/nba/teams/']

    def parse(self, response):
        teams = response.xpath("//a[starts-with(@href, '/nba/team/roster/_/name/')]/@href").extract()
        for team in teams:
            print(team)
