# -*- coding: utf-8 -*-
import scrapy


class RostersSpider(scrapy.Spider):
    name = 'rosters'
    allowed_domains = ['espn.com']
    start_urls = ['https://www.espn.com/nba/teams']

    def parse(self, response):
        rosterLinks = response.xpath("//a[starts-with(@href, '/nba/team/roster/_/name/')]/@href").extract()
        for rosterLink in rosterLinks:
            yield scrapy.Request('http://www.espn.com' + rosterLink, callback=self.parse_team)

    def parse_team(self, response):
        print("parsing team..." + response.url)
        playerLinks = response.xpath(".//tbody/tr/td[2]/span/a[starts-with(@href, 'http://www.espn.com/nba/player/_/id/')]")
        for playerLink in playerLinks:
            yield{
                'playerId': playerLink.xpath('@href').get(),
                'playerName': playerLink.xpath('text()').get()
            }