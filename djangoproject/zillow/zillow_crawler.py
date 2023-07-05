import os
import platform
import time

import pandas as pd
from bs4 import BeautifulSoup
# from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import requests

pd.set_option("display.max_columns", None)


class ZillowCrawler:
    def __init__(self):

        self.driver = None
        self.results = []
        self.listing_urls = ["https://www.zillow.com/new-york-ny-11236/"]

    def go_with_selenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        def interceptor(request):
            # del request.headers
            request.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br", "upgrade-insecure-requests": "1"}

        self.driver = webdriver.Chrome()
        self.driver.request_interceptor = interceptor

    def go_with_url(self, url):
        r = requests.get(url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'})
        return r.content

    def loop_over_listing_urls(self, go_with_selenium=False):
        data = None
        for item in self.listing_urls:
            data = self._get_listing_data(item, go_with_selenium=go_with_selenium)
            print(data)
        self.results.append(data)

    def _press_and_hold_for_captcha(self, element, sec=10):
        print('Passing by security check')
        print(element.text)
        action = ActionChains(self.driver)
        action.click_and_hold(element)
        action.perform()
        time.sleep(sec)
        action.release(element)
        action.perform()
        time.sleep(0.2)
        action.release(element)

    def _check_if_we_are_detected(self):
        element = self.driver.find_element('id', 'px-captcha')
        return element

    def security_check(self):
        element = self._check_if_we_are_detected()
        if element:
            self._press_and_hold_for_captcha(element)
            time.sleep(30)

    def _get_listing_data(self, target_url, go_with_selenium=False):

        resp = None
        if go_with_selenium:
            self.go_with_selenium()
            self.driver.get(target_url)
            time.sleep(1)  # time to boot up chrome browser
            self.security_check()

            html = self.driver.find_element('tag name', 'html')
            html.send_keys(Keys.END)
            time.sleep(3)  # time to load whole data
            resp = self.driver.page_source
            self.driver.close()

            print(resp)
        else:
            url = f"https://api.scrapingdog.com/scrape?api_key=649c53e10a13b35c882b97ce&url={target_url}&premium=true&country=us"
            resp = self.go_with_url(url)
            print(resp)

        soup = BeautifulSoup(resp, 'html.parser')
        properties_for_real_estate = soup.find_all("div", {
            "class": "StyledPropertyCardDataWrapper-c11n-8-69-2__sc-1omp4c3-0 KzAaq property-card-data"})

        result = []
        for x in range(0, len(properties_for_real_estate)):
            property_dict = {}
            try:
                property_dict["pricing"] = properties_for_real_estate[x].find("div", {
                    "class": "StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0 kJFQQX"}).text
            except:
                property_dict["pricing"] = None
            try:
                property_dict["size"] = properties_for_real_estate[x].find("div", {
                    "class": "StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0 bKFUMJ"}).text
            except:
                property_dict["size"] = None
            try:
                property_dict["address"] = properties_for_real_estate[x].find("a", {
                    "class": "StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0 dZxoFm property-card-link"}).text
            except:
                property_dict["address"] = None
            result.append(property_dict)

        return result


zc = ZillowCrawler()
zc.loop_over_listing_urls()
# time.sleep(60 * 60)
