# -*- coding: utf-8 -*-
import scrapy
import logging
import re

from fantasymanager_scrapy.items import StatisticItem, GameItem

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
        gameItem = GameItem()

        teamHomeDiv = response.css("div.team.home")
        teamAwayDiv = response.css("div.team.away")
        
        gameItem['teamHome'] = teamHomeDiv.xpath(".//a[starts-with(@href, '/nba/team/_/name/')]/@href").get()
        gameItem['teamHomeScore'] = teamHomeDiv.css("div.score.icon-font-before::text").get()
        gameItem['teamAway'] = teamAwayDiv.xpath(".//a[starts-with(@href, '/nba/team/_/name/')]/@href").get()
        gameItem['teamAwayScore'] = teamAwayDiv.css("div.score.icon-font-after::text").get()
        
        gameItem['statistics'] = []

        statisticHomeRows = response.css("div.col.column-two.gamepackage-home-wrap table.mod-data tbody tr")
        for statisticHomeRow in statisticHomeRows:
            if "highlight" <> statisticHomeRow.xpath("@class").get():
                statisticItem = self.parse_statistic(statisticHomeRow)
                gameItem['statistics'].append(statisticItem)

        statisticAwayRows = response.css("div.col.column-one.gamepackage-away-wrap table.mod-data tbody tr")
        for statisticAwayRow in statisticAwayRows:
            if "highlight" <> statisticAwayRow.xpath("@class").get():
                statisticItem = self.parse_statistic(statisticAwayRow)
                gameItem['statistics'].append(statisticItem)

        yield gameItem

    def parse_statistic(self, statisticElement):    
        statisticItem = StatisticItem()    
        
        playerLink = statisticElement.css("a[href*='/nba/player/_/id/']::attr(href)").get()
        nbaId = re.search('/nba/player/_/id/(.*)/', playerLink).group(1)
        # logging.info('nbaId: ' + nbaId)
        statisticItem['playerNbaId'] = nbaId

        return statisticItem