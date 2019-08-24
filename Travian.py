from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from values import *
import re
import time


class Travian:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password

        self.url = url

        self.browser = webdriver.Firefox()

        self.browser.get(self.url)

    def stop(self):
        self.browser.quit()

    def unzoom(self):
        self.browser.execute_script(
            'document.body.style.MozTransform = "scale(0.50)";')
        self.browser.execute_script(
            'document.body.style.MozTransformOrigin = "0 0";')

    def switchPage(self, page):
        self.browser.get(self.url+page)
        self.unzoom()

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

    # TODO Finish method
    def build(self, bid):
        if(self.checkBuildingAvailability(bid)):
            pass

    def sendArmy(self, coord, armyValues, type):
        if(self.returnLink() != actions['armySend']):
            self.switchPage(actions['armySend'])

        self.browser.find_element_by_id('xCoordInput').send_keys(coord[0])
        self.browser.find_element_by_id('yCoordInput').send_keys(coord[1])

        troops = self.browser.find_element_by_id('troops')

        for unit in troops.find_elements_by_css_selector('input'):
            index = int(unit.get_attribute('name')[1:]) - 1
            # print(index, str(armyValues[index]))
            if(armyValues[index]):
                unit.send_keys(str(armyValues[index]))

        options = self.browser.find_element_by_class_name('option')
        for radio in options.find_elements_by_css_selector('input'):
            if radio.get_attribute('value') == str(type):
                radio.click()

        self.browser.find_element_by_id('btn_ok').click()
        self.browser.find_element_by_id('btn_ok').click()

    def buildArmy(self, armyValues, max=False):
        if(self.returnLink() != actions['barracks']):
            self.switchPage(actions['barracks'])

        self.unzoom()

        for unit in self.browser.find_elements_by_class_name('details'):
            unitBox = unit.find_element_by_css_selector('input')
            index = int(unitBox.get_attribute('name')[1:]) - 1

            try:
                if(armyValues[index]):
                    # unit.send_keys(str(armyValues[index]))
                    if(max):
                        maxLink = unit.find_element_by_class_name(
                            'cta').find_element_by_css_selector('a')

                        if(int(maxLink.text)):
                            maxLink.click()
            except:
                print(index)

        self.browser.find_element_by_id('s1').click()

    def switchVillage(self, villageName):
        # TODO: check current page!

        villageList = self.browser.find_element_by_id('sidebarBoxVillagelist')

        for village in villageList.find_elements_by_css_selector('li'):
            if(village.find_element_by_class_name('name').text == villageName):
                # print(f'Found {villageName}')
                village.find_element_by_css_selector('a').click()
                break

        self.unzoom()

        # time.sleep(2)

    def villageList(self):
        list = []

        villageList = self.browser.find_element_by_id('sidebarBoxVillagelist')
        for village in villageList.find_elements_by_css_selector('li'):
            villageName = village.find_element_by_class_name('name').text

            villageCoordXRaw = village.find_element_by_class_name(
                'coordinateX').text
            villageCoordYRaw = village.find_element_by_class_name(
                'coordinateY').text

            print(villageCoordXRaw, villageCoordYRaw)

            for y in villageCoordYRaw:
                if y == '−‭':
                    print("True")

            villageCoordX = re.findall(r'\d+', villageCoordXRaw)
            villageCoordY = re.findall(r'\d+', villageCoordYRaw)

            villageCoordX = ''.join(villageCoordX)
            villageCoordY = ''.join(villageCoordY)

            # print(villageCoordX, villageCoordY)

            list.append(Village(villageName, villageCoordX, villageCoordY))

        return list

    def checkRaid(self, seconds=False):
        if(self.returnLink() != actions['armyMovement']):
            self.switchPage(actions['armyMovement'])

        raids = []

        raidTable = self.browser.find_elements_by_class_name('inRaid')

        for el in raidTable:
            timingIn = el.find_element_by_class_name('in').text[3:-5]
            raids.append(timingIn)

        if seconds:
            attackSeconds = []

            for time in raids:
                seconds = sum(x * int(t)
                              for x, t in zip([3600, 60, 1], time.split(":")))
                attackSeconds.append(seconds)

            return attackSeconds

        return raids

    def quickFS(self, coord, type, gapTime):
        if(self.returnLink() != actions['armySend']):
            self.switchPage(actions['armySend'])

        troops = self.browser.find_element_by_id('troops')

        # Number of sent troops
        total = 0

        for unit in troops.find_elements_by_css_selector('a'):
            total += 1
            unit.click()

        if not total:
            # Nothing to send
            return

        self.browser.find_element_by_id('xCoordInput').send_keys(str(coord[0]))
        self.browser.find_element_by_id('yCoordInput').send_keys(str(coord[1]))

        options = self.browser.find_element_by_class_name('option')
        for radio in options.find_elements_by_css_selector('input'):
            if radio.get_attribute('value') == str(type):
                radio.click()

        self.browser.find_element_by_id('btn_ok').click()
        self.browser.find_element_by_id('btn_ok').click()

        self.switchPage(actions['armyMovement'])
        self.unzoom()

        time.sleep(min(gapTime, 90))

        element = 'outSupply'

        if type == 4:
            element = 'outRaid'
            # TODO: type == 3

        army = self.browser.find_elements_by_class_name(element)

        for unit in army:
            try:
                unit.find_element_by_tag_name('button').click()
                print('Returning army')
                break
            except:
                pass

    def longFS(self, coord, type):
        if(self.returnLink() != actions['armySend']):
            self.switchPage(actions['armySend'])

        troops = self.browser.find_element_by_id('troops')

        # Number of sent troops
        total = 0

        for unit in troops.find_elements_by_css_selector('a'):
            total += 1
            unit.click()

        if not total:
            # Nothing to send
            return

        self.browser.find_element_by_id('xCoordInput').send_keys(str(coord[0]))
        self.browser.find_element_by_id('yCoordInput').send_keys(str(coord[1]))

        options = self.browser.find_element_by_class_name('option')
        for radio in options.find_elements_by_css_selector('input'):
            if radio.get_attribute('value') == str(type):
                radio.click()

        self.browser.find_element_by_id('btn_ok').click()
        self.browser.find_element_by_id('btn_ok').click()


class Village:
    def __init__(self, name, coordX, coordY):
        self.name = name
        self.coordX = coordX
        self.coordY = coordY
