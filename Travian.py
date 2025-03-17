from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from PIL import Image
import pytesseract
from io import BytesIO

import re
import time
from pprint import pprint

from values import *

class Travian:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password

        self.url = url

        self.browser = webdriver.Firefox()
        self.browser.set_window_position(-1920,0)
        #Tesseract-OCR
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\hormot\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
        self.browser.find_element('name','user').send_keys(self.username)
        self.browser.find_element('name','pw').send_keys(self.password)
        # self.browser.find_element('id','lowRes').click()

        #TODO: Monitor captcha input
        captcha_element = self.browser.find_element(By.CLASS_NAME, 'captcha').find_element(By.TAG_NAME, 'img')
        captcha_image = captcha_element.screenshot_as_png

        image = Image.open(BytesIO(captcha_image))
        custom_config = r'--oem 1 --psm 9 -c tessedit_char_whitelist=0123456789'
        captcha_text = pytesseract.image_to_string(image, config=custom_config)
        # captcha_text = pytesseract.image_to_string(image, config='--psm 8 --oem 3')

        captcha_input = self.browser.find_element(By.NAME, 'captcha').send_keys(captcha_text)

        while self.returnLink() != links['resources']:
            time.sleep(0.5)

        # self.browser.find_element('id', 's1').click()

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

        resStorageRaw = self.browser.find_element(By.ID, 'res')
        self.resStorage = [int(el.text.split('/')[0]) for el in resStorageRaw.find_elements(By.TAG_NAME, "li")]

        # self.resStorageFreeFood = self.resStorage[-1]
        self.resProduction = self.resStorage[:-1]

    def mapStorage(self):
        if(self.returnLink() != links['resources']):
            self.switchResources()

        resStorageRaw = self.browser.find_element(By.ID, 'res')
        self.resStorage = [int(el.text.split('/')[-1]) for el in resStorageRaw.find_elements(By.TAG_NAME, "li")]

        self.resStorageFreeFood = self.resStorage[-1]
        self.resStorage = self.resStorage[:-1]

    def checkCost(self, cost):
        if(cost[0] <= self.resStorage[0] and cost[1] <= self.resStorage[1] and
                cost[2] <= self.resStorage[2] and cost[3] <= self.resStorage[3]):
            return True

        return False

    def checkBuildingAvailability(self, bid):
        self.switchBuilding(bid)

        buildingCostRaw = self.browser.find_element('id', 'contract')

        self.buildingCost = [
            int(re.sub(r'[\D]', '', el.text)) for el in buildingCostRaw.find_elements(By.CLASS_NAME, "value")]

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

        self.browser.find_element('id', 'xCoordInput').send_keys(coord[0])
        self.browser.find_element('id', 'yCoordInput').send_keys(coord[1])

        troops = self.browser.find_element('id', 'troops')

        for unit in troops.find_elements(By.CSS_SELECTOR, 'input'):
            index = int(unit.get_attribute('name')[1:]) - 1
            # print(index, str(armyValues[index]))
            if(armyValues[index]):
                unit.send_keys(str(armyValues[index]))

        options = self.browser.find_element(By.CSS_SELECTOR, 'option')
        for radio in options.find_elements(By.CSS_SELECTOR, 'input'):
            if radio.get_attribute('value') == str(type):
                radio.click()

        self.browser.find_element('id', 'btn_ok').click()
        self.browser.find_element('id', 'btn_ok').click()

    def buildArmy(self, armyValues, max=False):
        if(self.returnLink() != actions['barracks']):
            self.switchPage(actions['barracks'])

        self.unzoom()

        for unit in self.browser.find_elements(By.CLASS_NAME, 'details'):

            div = unit.find_element(By.TAG_NAME, 'div')
            if div:
                self.browser.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                """, div)

            unitBox = unit.find_elements(By.CSS_SELECTOR, 'a')
            #TODO: Build more than tier 1 units
            for link in unitBox:
                if max:
                    link.click()
                    self.browser.find_element(By.ID, 'btn_train').click()
                    break

        self.browser.find_element('id', ('s1')).click()

    def switchVillage(self, villageName):
        # TODO: check current page!

        villageList = self.browser.find_element('id', ('sidebarBoxVillagelist'))

        for village in villageList.find_elements(By.CSS_SELECTOR, 'li'):
            if(village.find_element(By.CLASS_NAME, 'name').text == villageName):
                # print(f'Found {villageName}')
                village.find_element_by_css_selector('a').click()
                break

        self.unzoom()

        # time.sleep(2)

    def villageList(self):
        list = []

        villageList = self.browser.find_element('id', 'villageList')

        for village in villageList.find_elements(By.CSS_SELECTOR, 'li'):
            villageName = village.find_element(By.TAG_NAME, 'a').text

            #TODO: Fix missing coordinates
            tooltipText = village.find_element(By.TAG_NAME, 'a').get_attribute('title')

            list.append((villageName, tooltipText))

        return list

    def checkRaid(self, seconds=False):
        if(self.returnLink() != actions['armyMovement']):
            self.switchPage(actions['armyMovement'])

        raids = []

        raidTable = self.browser.find_elements(By.CLASS_NAME, 'inRaid')

        for el in raidTable:
            timingIn = el.find_element(By.CLASS_NAME, 'in').text[3:-5]
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

        troops = self.browser.find_element('id', ('troops'))

        # Number of sent troops
        total = 0

        for unit in troops.find_elements(By.CSS_SELECTOR, 'a'):
            total += 1
            unit.click()

        if not total:
            # Nothing to send
            return

        self.browser.find_element('id', ('xCoordInput').send_keys(str(coord[0])))
        self.browser.find_element('id', ('yCoordInput').send_keys(str(coord[1])))

        options = self.browser.find_element(By.CLASS_NAME, 'option')
        for radio in options.find_elements(By.CSS_SELECTOR, 'input'):
            if radio.get_attribute('value') == str(type):
                radio.click()

        self.browser.find_element('id', ('btn_ok')).click()
        self.browser.find_element('id', ('btn_ok')).click()

        self.switchPage(actions['armyMovement'])
        self.unzoom()

        time.sleep(min(gapTime, 90))

        element = 'outSupply'

        if type == 4:
            element = 'outRaid'
            # TODO: type == 3

        army = self.browser.find_elements(By.CLASS_NAME, element)

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

        troops = self.browser.find_element('id', ('troops'))

        # Number of sent troops
        total = 0

        for unit in troops.find_elements(By.CSS_SELECTOR, 'a'):
            total += 1
            unit.click()

        if not total:
            # Nothing to send
            return

        self.browser.find_element('id', ('xCoordInput').send_keys(str(coord[0])))
        self.browser.find_element('id', ('yCoordInput').send_keys(str(coord[1])))

        options = self.browser.find_element(By.CLASS_NAME, 'option')
        for radio in options.find_elements(By.CSS_SELECTOR, 'input'):
            if radio.get_attribute('value') == str(type):
                radio.click()

        self.browser.find_element('id', ('btn_ok')).click()
        self.browser.find_element('id', ('btn_ok')).click()

    def set_village_levels_visible(self):
        if(self.returnLink() != links['buildings']):
            self.switchPage(links['buildings'])

        element = self.browser.find_element(By.ID, 'levels')
        self.browser.execute_script("arguments[0].setAttribute('class', 'on')", element)

    def get_buildings_and_levels(self):
        if(self.returnLink() != links['buildings']):
            self.switchPage(links['buildings'])

        self.set_village_levels_visible()

        clickareas = self.browser.find_element(By.ID, 'village_map')
        img_tags = clickareas.find_elements(By.TAG_NAME, 'img')

        buildings = [(img.get_attribute('alt'), img.get_attribute('class')) for img in img_tags]

        def insert_spaces(text):
            text_array = re.sub(r'([a-z])([A-Z0-9])', r'\1 \2', text)

            if text_array == "Construction site":
                return (text_array, 0)

            text_array = text_array.replace("Level", "")

            text_array = text_array.split(" ")
            return (" ".join(text_array[:-1]).strip(), text_array[-1])

        # Get a list of building sites
        buildings = [insert_spaces(img.get_attribute('alt')) for img in img_tags]

        # Remove empty sites and empty touples
        buildings = [building for building in buildings if "Construction site" not in building[0] and building[0] != ""]
        
        # Convert the second element of the tuple into an integer
        buildings = [(building[0], int(building[1])) for building in buildings]  

        buildings_dict = {}
        for building in buildings:
            if building[0] not in buildings_dict:
                buildings_dict[building[0]] = [building[1]]
            else:
                buildings_dict[building[0]].append(building[1])
        
        return buildings_dict

    def get_resource_levels(self):
        if(self.returnLink() != links['resources']):
            self.switchPage(links['resources'])

        village_map = self.browser.find_element(By.ID, 'village_map')
        level_divs = village_map.find_elements(By.CLASS_NAME, 'level')
        resource_levels = [int(div.text) for div in level_divs if div.text.isdigit()]

        return resource_levels
    
    def switch_resource(self, id):
        # if(self.returnLink() != actions['resource']):
        self.switchPage(f"{actions['resource']}{id}")

    def build_field(self, id):
        self.switch_resource(id)

        try:
            # build_button = self.browser.find_element(By.XPATH, "//button[@value='Upgrade level']")
            contract_element = self.browser.find_element(By.ID, 'contract')

            build_button = contract_element.find_element(By.TAG_NAME, 'button')
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(build_button))
            
            clock_element = contract_element.find_element(By.CLASS_NAME, 'clocks')
            clock_text = clock_element.text

            h, m, s = map(int, clock_text.split(':'))
            total_seconds = h * 3600 + m * 60 + s

            build_button.click()

            while self.returnLink() != links['resources']:
                time.sleep(0.5)

            return total_seconds
        except:
            return False
        
    def max_resources(self, max_level = 10):
        resource_levels = self.get_resource_levels()

        for index, level in enumerate(resource_levels):
            while level < max_level:
                print(f"Building field at index {index} with current level {level}")
                wait = self.build_field(index + 1)

                if wait:
                    time.sleep(wait)  # Adjust sleep time as needed

                resource_levels = self.get_resource_levels()
                level = resource_levels[index]

    def get_warehouse_level(self):
        pass

    def id_matcher(self):
        id_range = range(1, 39)

        id_list = {}

        tabs = []

        for id in id_range:
            self.browser.execute_script(f"window.open('');")
            self.browser.switch_to.window(self.browser.window_handles[-1])
            self.browser.get(f'{self.url}build.php?id={id}')
            tabs.append(self.browser.current_window_handle)

        for tab in tabs:
            self.browser.switch_to.window(tab)
            try:
                WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='titleInHeader']")))

                header = self.browser.find_element(By.XPATH, "//h1[@class='titleInHeader']")
                building_name = header.text.split(" Level")[0]

                id_list[building_name] = id

                # print(f"ID: {id}, Title: {header.text}")
                self.browser.close()
            except:
                pass

        return id_list

    def check_if_building(self, name):
        buildings = self.get_buildings_and_levels()

        for building in buildings:
            if building[0] == name:
                return True
            
        return False
    
    def build_new_building(self, name):
        is_built = self.check_if_building(name)

        if not is_built:
            self.switchPage(actions['construction'])

            try:
                content_div = self.browser.find_element(By.ID, 'build')
                headers = content_div.find_elements(By.TAG_NAME, 'h2')
                buttons = content_div.find_elements(By.TAG_NAME, 'button')

                for idx, header in enumerate(headers):
                    if header.text == name:
                        buttons[idx].click()

                        while self.returnLink() != links['buildings']:
                            time.sleep(0.5)

                        return True
            except:
                return False
            
        return False
    
    def upgrade_building(self, id):
        link_suffix = f"{actions['city']}{id}"
        self.switchPage(link_suffix)

        try:
            # Check if already max update
            contract_element = self.browser.find_element(By.ID, 'content')
            if "completely upgraded" in contract_element.text:
                return 0

            max_refresh = 5
            for idx in range(max_refresh):
                try:
                    contract_element = self.browser.find_element(By.ID, 'contract')
                    break
                except:
                    print(f"Retrying upgrade attempt: {idx}")
                    self.browser.refresh()
                    time.sleep(0.5)

            build_button = contract_element.find_element(By.TAG_NAME, 'button')
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(build_button))
            
            clock_element = contract_element.find_element(By.CLASS_NAME, 'clocks')
            clock_text = clock_element.text

            h, m, s = map(int, clock_text.split(':'))
            total_seconds = h * 3600 + m * 60 + s

            build_button.click()

            while self.returnLink() != links['buildings']:
                time.sleep(0.5)

            return total_seconds
        except Exception as e:
            print(e)
            return False
        
    def max_buildings(self, buildings, level=20):
        ids = self.id_matcher()
        levels = self.get_buildings_and_levels()

        building_dict = {}
        for building in buildings:
            if not building in list(levels.keys()):
                print(f'{building} not found')
                continue

            if not building in list(ids.keys()):
                continue

            building_dict[building] = {
            'level': levels[building] if levels[building] else None,
            'id': ids[building] if ids[building] else None
            }

        for key, building in building_dict.items():
            building_id = building['id']
            building_level = building['level'][0]

            if building_level >= level:
                print(f'{key}: Level already satisfied')
                continue

            if building_level < level:
                pprint(f'{key}: id: {building_id} level: {building_level}')

                for i in range(building_level, level):
                    print(f'Upgrading {building} to level {i + 1}. Building ID is {building_id}')
                    wait = self.upgrade_building(building_id)

                    if wait == False:
                        time.sleep(wait+1)
                    else:
                        print(f"Failed to upgrade {key} at level {i}")
                        break

        return True

class Village:
    def __init__(self, name, coordX, coordY):
        self.name = name
        self.coordX = coordX
        self.coordY = coordY
