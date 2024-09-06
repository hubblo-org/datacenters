#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pprint import pprint
import pandas as pd
from datetime import datetime, timezone

folder = "."

def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument("--no-sandbox")
    #options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    #options.add_argument("--remote-debugging-port=9222")  # this
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--disable-dev-shm-using")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument(r"user-data-dir=.\cookies\\test")
    driver = webdriver.Chrome(options)

    detail_urls = []
    for page in range(1,19):
        driver.get("https://carte.dcmag.fr/?_page={}".format(page))

        items = driver.find_elements(By.CSS_SELECTOR, ".drts-entity-post")
        print("found {} items".format(len(items)))
        for i in items:
            try:
                link = i.find_element(By.TAG_NAME, "a")
                print("{}".format(link.text))
                detail_urls.append(link.get_property("href"))
            except:
                print("no link found")

    # prepare new data for csv

    df = pd.DataFrame({
        'id': [],
        'name': [],
        'owner': [],
        'address': [],
        'city': [],
        'postal_code': [],
        'region': [],
        'country': [],
        'country_code': [],
        'cadastral_id': [],
        'power_installed': [],
        'square_ft_meters_global': [],
        'square_ft_meters_it': [],
        'date_of_building_manufacturing': [],
        'date_of_land_buying_act': [],
        'main_source': [],
        'secondary_source': [],
        'last_update': [],
        'comment_main_source': [],
        'comment_secondary_source': [],
    })
    pprint(detail_urls)
    for u in detail_urls:
        driver.get(u)
        #for p in ["street_address", "locality", "region", "postal_code", "country_name"]:
        #    name = "business:contact_data:{}".format(p)
        #    meta = driver.find_elements(By.XPATH, "//meta[@property='{}']".format(name))
        #    print("prop={} content={}".format(name.split(":")[-1], meta[0].get_property("content")))
        datacenter_name = driver.find_element(By.TAG_NAME, "h1")
        country_code = driver.find_elements(By.XPATH, "//meta[@property='business:contact_data:country_name']")[0].get_property("content")
        utc_dt = datetime.now(timezone.utc)
        new_entry = pd.DataFrame({
            'id': ["{}".format(datacenter_name.text.replace(" ", "_"))],
            'name': [datacenter_name.text],
            'owner': [None],
            'address': [driver.find_elements(By.XPATH, "//meta[@property='business:contact_data:street_address']")[0].get_property("content")],
            'city': [driver.find_elements(By.XPATH, "//meta[@property='business:contact_data:locality']")[0].get_property("content")],
            'postal_code': [driver.find_elements(By.XPATH, "//meta[@property='business:contact_data:postal_code']")[0].get_property("content")],
            'region': [driver.find_elements(By.XPATH, "//meta[@property='business:contact_data:region']")[0].get_property("content")],
            'country': ["France" if country_code == "FR" else "Switzerland" if country_code == "CH" else "Belgium" if country_code == "BE" else "Monaco" if country_code == "MC" else "Luxemburg" if country_code == "LU" else country_code],
            'country_code': [country_code],
            'cadastral_id': [None],
            'power_installed': [None],
            'square_ft_meters_global': [None],
            'square_ft_meters_it': [None],
            'date_of_building_manufacturing': [None],
            'date_of_land_buying_act': [None],
            'main_source': ["carte.dcmag.fr"],
            'secondary_source': [None],
            'last_update': [utc_dt.astimezone().isoformat()],
            'comment_main_source': ["scraped from website with selenium"],
            'comment_secondary_source': [None],
        })
        print("Adding {}".format(new_entry))
        df = pd.concat([df, new_entry])

    df.to_csv("output_carte.dcmag.fr.csv")

if __name__ == '__main__':
    main()
