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

    def returnLink(self):
        return self.browser.current_url[(len(self.url)):]

    def switchResources(self):
        self.switchPage(links['resources'])
        self.housekeepingResources()

    def switchBuildings(self):
        self.switchPage(links['buildings'])

    def switchBuilding(self, bid):
        self.switchPage(actions['building']+f'?id={bid}')

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

        self.housekeepingResources()

    def housekeepingResources(self):
        if(self.returnLink() != links['resources']):
            self.switchResources()

        self.mapProduction()
        self.mapStorage()

        # print(self.resProduction)
        # print(self.resStorage)

    # TODO: Finish method

    def mapResourceFields(self):
        links = self.browser.find_elements_by_partial_link_text(
            'build.php?id=')
        print(links)

    def mapProduction(self):
        if(self.returnLink() != links['resources']):
            self.switchResources()

        self.resProduction = [
            int(re.findall(r'\d+', el.text)[0]) for el in self.browser.find_elements_by_class_name("num")][:4]

    def mapStorage(self):
        resStorageRaw = self.browser.find_element_by_id('stockBar')

        self.resStorageAll = [int(re.sub(r'[\D]', '', el.text))
                              for el in resStorageRaw.find_elements_by_class_name("value")]

        self.resStorageMax = [self.resStorageAll[0], self.resStorageAll[4]]
        self.resStorage = [self.resStorageAll[1],
                           self.resStorageAll[2],
                           self.resStorageAll[3],
                           self.resStorageAll[5]
                           ]
        self.resStorageFreeFood = self.resStorageAll[-1]

        # print(self.resStorageMax)
        # print(self.resStorage)
        # print(self.resStorageFreeFood)

    def checkCost(self, cost):
        if(cost[0] <= self.resStorage[0] and cost[1] <= self.resStorage[1] and
                cost[2] <= self.resStorage[2] and cost[3] <= self.resStorage[3]):
            return True

        return False

    def checkBuildingAvailability(self, bid):
        self.switchBuilding(bid)

        buildingCostRaw = self.browser.find_element_by_id(
            'contract')

        self.buildingCost = [
            int(re.sub(r'[\D]', '', el.text)) for el in buildingCostRaw.find_elements_by_class_name("value")]

        for x in range(3):
            print(self.buildingCost[x], self.resStorage[x])

        # print(self.buildingCost)
        if(self.checkCost(self.buildingCost)):
            return True

        return False

    def build(self, bid):
        if(self.checkBuildingAvailability(bid)):
            pass

    def sendArmy(self, xCoord, yCoord, armyValues):
        if(self.returnLink() != actions['armySend']):
            self.switchPage(actions['armySend'])

        self.browser.find_element_by_id('xCoordInput').send_keys(xCoord)
        self.browser.find_element_by_id('yCoordInput').send_keys(yCoord)

        troops = self.browser.find_element_by_id('troops')

        for unit, quant in zip(troops.find_elements_by_css_selector('input'), armyValues):
            unit.send_keys(str(quant))
