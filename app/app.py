from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

import os
import time
import selenium
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)


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
        chrome_options.binary_location = os.environ.get(
            'GOOGLE_CHROME_BIN',
            "chromedriver"
        )
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")
        self.driver = selenium.webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"),
            options=chrome_options)

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



# Maps names to Strava URLs
QUERY_MAP = {
    'Miles': "https://www.strava.com/athletes/336687/segments/leader",
    'Lee': "https://www.strava.com/athletes/15315238/segments/leader",
}


# Cache that stores recently-fetched results
results_cache = {}


def refresh_cache():
    print("Refreshing cache")
    for name in QUERY_MAP.keys():
        koms = engine.query(name)
        results_cache[name] = koms


# Engine for querying Strava
engine = QueryEngine(QUERY_MAP)
# initially populate the cache
refresh_cache()


def query_and_add_name_to_cache(name):
    results_cache[name] = engine.query(name)


# Schedule a cache refresh every 30 minutes so Strava
# doesn't block whatever random linux box this is running on.
# Don't query on pageload because Strava is so so so slow
scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_cache, trigger="interval", seconds=1800)
scheduler.start()


@app.route('/koms')
def koms():
    results = {}
    for name in QUERY_MAP.keys():
        # cache miss -- query
        if name not in results_cache.keys():
            query_and_add_name_to_cache(name)

        results[name] = results_cache[name]
    return results
