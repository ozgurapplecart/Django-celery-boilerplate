from seleniumwire import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import os
import zipfile
from datetime import date

class MekanComFetcher:
    def __init__(self):
        self.driver = None

    def run(self):
        resp = self.driver.page_source
        soup = BeautifulSoup(resp, 'html.parser')
        total_page_number = int(soup.find('ul', {"class": "pagination"}).find_all('li')[-1].text)
        current_page = int(
            soup.find('ul', {"class": "pagination"}).find_all('li', {"class": "selected active"})[0].text)
        list_of_cities = [item['value'].replace('https://mekan.com/yeme-icme/c/', '').replace('/o/bar', '') for item in
                          soup.find('select', {"id": "city"}).find_all('option') if '/c/' in item['value']]
        self.driver.get(f'https://mekan.com/yeme-icme/c/istanbul/i/adalar/o/bar?p=1')

        for il in list_of_cities:
            for tip in ['bar', 'cafe']:
                self.driver.get(f'https://mekan.com/yeme-icme/c/{il}/')
                time.sleep(2)
                resp = self.driver.page_source
                soup = BeautifulSoup(resp, 'html.parser')

                ilce_list = [
                    item['value'].replace(f'https://mekan.com/yeme-icme/c/{il}/i/', '').replace(f'/o/{tip}', '') for
                    item in soup.find('select', {"id": "town"}).find_all('option') if '/i/' in item['value']]

                for ilce in ilce_list:
                    mekan_isimleri = []
                    mekan_linkleri = []
                    mekan_sehirleri = []
                    mekan_sokak_adresleri = []
                    mekan_ratingleri = []

                    page_number = 1
                    total_page_number = 10

                    while True:
                        if (page_number > total_page_number):
                            break
                        print(page_number, total_page_number)
                        print(f'https://mekan.com/yeme-icme/c/{il}/i/{ilce}/o/{tip}?p={page_number}')
                        self.driver.get(f'https://mekan.com/yeme-icme/c/{il}/i/{ilce}/o/{tip}?p={page_number}')
                        resp = self.driver.page_source
                        soup = BeautifulSoup(resp, 'html.parser')
                        time.sleep(4)

                        try:
                            print(1)
                            total_page_number = int(soup.find('ul', {"class": "pagination"}).find_all('li')[-1].text)
                        except Exception as e:
                            try:
                                print(2)
                                total_page_number = int(
                                    soup.find('ul', {"class": "pagination"}).find_all('li')[-3].text)
                                print(total_page_number)
                            except Exception as e:
                                total_page_number = -1
                                print(3)

                        print(il, ilce, total_page_number)
                        mekan_isimleri += [mekan.text for mekan in soup.find_all('a', {"itemprop": "name"})]
                        mekan_linkleri += [mekan.href for mekan in soup.find_all('a', {"itemprop": "name"})]
                        mekan_sehirleri += [mekan.text for mekan in soup.find_all('b', {"itemprop": "addressLocality"})]
                        mekan_sokak_adresleri += [mekan.text for mekan in
                                                  soup.find_all('span', {"itemprop": "streetAddress"})]
                        mekan_ratingleri += [int(mekan['content']) for mekan in
                                             soup.find_all('meta', {"itemprop": "ratingValue"})]
                        page_number += 1

                    DF = pd.DataFrame(np.array([mekan_isimleri, mekan_linkleri, mekan_sehirleri, mekan_sokak_adresleri,
                                                mekan_ratingleri])).transpose()
                    DF.to_csv(f'mekan_com_data_{il}_{ilce}_{tip}.csv')

    def setup(self):
        def interceptor(request):
            request.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br", "upgrade-insecure-requests": "1"
            }

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument("--incognito")
        options.add_argument("--incognito")
        options.add_argument("--headless")

        # add acceptInsecureCerts
        capabilities = options.to_capabilities()
        capabilities['acceptInsecureCerts'] = True

        proxy_options = {
            #     'proxy': {
            #         'http': "http://scrapingdog:649c53e10a13b35c882b97ce-country=us@proxy.scrapingdog.com:8081",
            #         'https': "https://scrapingdog:649c53e10a13b35c882b97ce-country=us@proxy.scrapingdog.com:8081",
            #     }
        }
        self.driver = webdriver.Chrome(options=options, seleniumwire_options=proxy_options)
        self.driver.request_interceptor = interceptor
        self.driver.get(f'https://mekan.com/yeme-icme/c/istanbul/i/kadikoy/o/bar?p=1')
        time.sleep(2)

    def prepare_results(self):
        today = date.today()
        fname = f'{str(today)}_mekan_com_data.zip'
        zf = zipfile.ZipFile(fname, "w")
        for dirname, subdirs, files in os.walk("./"):
            zf.write(dirname)
            for filename in files:
                if '.csv' in filename:
                    print(filename)
                    path = os.path.join(dirname, filename)
                    zf.write(path)
                    os.remove(path)
        zf.close()
        return fname

