# -*- coding: utf-8 -*-
import scrapy


class RostersSpider(scrapy.Spider):
    name = 'rosters'
    allowed_domains = ['espn.com']
    start_urls = ['https://www.espn.com/nba/teams']

    def parse(self, response):
        teams = response.xpath("//a[starts-with(@href, '/nba/team/roster/_/name/')]/@href").extract()
        for team in teams:
            yield scrapy.Request('http://www.espn.com' + team, callback=self.parse_team)

    def parse_team(self, response):
        print("parsing team...")