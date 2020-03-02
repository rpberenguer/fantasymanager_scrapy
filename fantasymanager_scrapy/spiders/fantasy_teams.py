# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FantasyTeamsSpider(Spider):
    name = 'fantasy_teams'
    allowed_domains = ['fantasy.espn.com']
    start_urls = ['http://fantasy.espn.com/basketball/league/rosters?leagueId=97189']

    def __init__(self):
        # self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=options)

    def parse(self, response):        
        self.driver.get(response.url)

        wait = WebDriverWait(self.driver, 20)

        wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe#disneyid-iframe")))

        # sel = Selector(text=self.driver.page_source)
        # # email = sel.find_element_by_xpath("//input[@type='email']")

        email = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))
        email.send_keys('rpberenguer@gmail.com')

        password = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        password.send_keys('ilovethisgame&&&')

        signupButton = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-submit ng-isolate-scope']")))
        signupButton.click()

        self.driver.switch_to.default_content()

        fantasyTeamList = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class='pa1 bg-clr-white br-5 roster-container']")))

        for fantasyTeamElement in fantasyTeamList:
            yield {'fantasyTeamName': fantasyTeamElement.find_element_by_css_selector('span.teamName.truncate').text}

        print ("Page is ready!")
