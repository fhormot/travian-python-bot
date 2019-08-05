from selenium import webdriver
import re
from values import *


class Travian:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password

        self.url = url

        self.browser = webdriver.Firefox()
        self.browser.get(self.url)

    def stop(self):
        self.browser.quit()

    def switchPage(self, page):
        self.browser.get(self.url+page)

    def switchResources(self):
        self.switchPage(links['resources'])

    def switchBuildings(self):
        self.switchPage(links['buildings'])

    def switchMap(self):
        self.switchPage(links['map'])

    def switchReports(self):
        self.switchPage(links['reports'])

    def login(self):
        self.browser.find_element_by_class_name(
            'text').send_keys(self.username)
        self.browser.find_element_by_name('password').send_keys(self.password)
        self.browser.find_element_by_id('lowRes').click()
        self.browser.find_element_by_id('s1').click()

    def mapResources(self):
        links = self.browser.find_elements_by_partial_link_text(
            'build.php?id=')
        print(links)

    def mapProduction(self):
        self.switchResources()

        resName = [
            el.text for el in self.browser.find_elements_by_class_name("res")]
        resVal = [
            int(re.findall(r'\d+', el.text)[0]) for el in self.browser.find_elements_by_class_name("num")]

        #resName = self.browser.find_elements_by_class_name('res')
        #resVal = self.browser.find_elements_by_class_name('num')

        for elN, elV in zip(resName, resVal):
            print(f'{elN} {elV}')
