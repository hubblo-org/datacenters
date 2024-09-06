#!/usr/bin/env python3

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://immobilier.pappers.fr")
driver.quit()
