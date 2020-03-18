from scrapy.item import Item, Field


class GameItem(Item):
    teamHome = Field()
    teamHomeScore = Field()
    teamAway = Field()
    teamAwayScore = Field()
    statistics = Field()

class StatisticItem(Item):
    playerNbaId = Field()