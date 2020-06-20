# -*- coding: utf-8 -*-
"""
DJM 6/17/2020
JDK 6/19/2020

DJM: notes: crashes on Lee when i dont use my 
personal login (which im not using here)
his accoutn private

JDK: refactored into a stateful engine so we don't start 
and orphan tons of webdriver processes
"""

import time
import selenium
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class QueryEngine(object):
    def __init__(self, url_map):
        self.url_map = url_map
        self.data = {}
        for key in url_map.keys():
            self.data[key] = 0
        self._initialize_webdriver()
        self.logged_in = False

    def _initialize_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = selenium.webdriver.Chrome(
            ChromeDriverManager()
            .install(), options=chrome_options)

    def _go_to_url_and_login(self, url):
        self.driver.get(url)
        if not self.logged_in:
            self.driver.find_element_by_id("email").send_keys(
                "aaronb11999933@gmail.com")
            self.driver.find_element_by_id(
                "password").send_keys("LeevsMilesKOM")
            self.driver.find_element_by_id("login-button").click()
            time.sleep(5)
            self.logged_in = True

    def query(self, name):
        if name not in self.url_map.keys():
            raise LookupError(
                f"Name {name} is not in lookup map "
                "used to initialize this query engine")
        self._go_to_url_and_login(self.url_map[name])
        # query
        KOMs = 0
        for tr in self.driver.find_elements_by_xpath(
                '/html/body/div[1]/div[3]/div[3]/div[1]/div/table'):
            tds = tr.find_elements_by_tag_name('td')
            for td in tds:
                if td.text == 'Ride':
                    KOMs += 1
        return KOMs

    def shutdown(self):
        self.driver.quit()


