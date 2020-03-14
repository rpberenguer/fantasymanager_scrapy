# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TransactionsSpider(Spider):
    name = 'transactions'
    allowed_domains = ['fantasy.espn.com']
    start_urls = ['http://fantasy.espn.com/basketball/recentactivity?leagueId=97189']

    def __init__(self):
        # self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        # options.add_argument('--headless')
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

        password = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        password.send_keys('ilovethisgame&&&')

        signupButton = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-submit ng-isolate-scope']")))
        signupButton.click()

        self.driver.switch_to.default_content()

        paginationNavList = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.PaginationNav__wrap.overflow-x-auto ul li a")))

        for paginationNavElement in reversed(paginationNavList):

            self.driver.execute_script("arguments[0].click();", paginationNavElement) 

            transactionList = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='transactionCell']")))

            # for transaction in transactionList:
            #     divTransactionDate = self.driver.find_element_by_xpath("../../../../td[1]/div/div")
            #     print("Transaction: " + divTransactionDate)

        print ("Page is ready!")
