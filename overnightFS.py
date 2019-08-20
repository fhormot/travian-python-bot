from Travian import Travian
from userData import *

import time

villages = ['Jo', 'Joo']
fsVillage = ['13', '-83']

T = Travian(username, password, url_main_x3)
T.login()

while True:
    for village in villages:
        T.switchVillage(village)

        attackSeconds = T.checkRaid(seconds=True)

        if not attackSeconds:
            continue

        print(f'{village}[{len(attackSeconds)}]: {attackSeconds[0]}')

        if attackSeconds[0] <= 9:
            # Less than 9 seconds to attack
            try:
                T.buildArmy([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], max=True)
                T.quickFS(fsVillage, 4)
            except:
                T.stop()
