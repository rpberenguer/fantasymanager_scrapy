# -*- coding: utf-8 -*-
import scrapy


class StatisticsSpider(scrapy.Spider):
    name = 'statistics'
    allowed_domains = ['espn.com']

    def __init__(self, startDate=None, *args, **kwargs):
        super(StatisticsSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.espn.com/nba/schedule/_/date/%s' % startDate]

    def parse(self, response):
        tableDayList = response.css("table.schedule.has-team-logos.align-left")
        
        for tableDay in tableDayList:
            gameLinks = tableDay.xpath(".//tbody/tr/td[1]/a[starts-with(@href, '/nba/team/_/name/')]/../../td[2]/div/a[starts-with(@href, '/nba/team/_/name/')]/../../../td[3]/a[starts-with(@href, '/nba/game?gameId=')]/@href").getall()

            for gameLink in gameLinks:
                yield scrapy.Request('http://www.espn.com/nba/boxscore?gameId=' + gameLink[17:], callback=self.parse_game)

    def parse_game(self, response):
        print("parsing game..." + response.url)
        teamHomeDiv = response.css("div.team.home")
        teamAwayDiv = response.css("div.team.away")
        yield{
            'teamHome': teamHomeDiv.xpath(".//a[starts-with(@href, '/nba/team/_/name/')]/@href").get(),
            'teamHomeScore': teamHomeDiv.css("div.score.icon-font-before::text").get(),
            'teamAway': teamAwayDiv.xpath(".//a[starts-with(@href, '/nba/team/_/name/')]/@href").get(),
            'teamAwayScore': teamAwayDiv.css("div.score.icon-font-after::text").get()
        }