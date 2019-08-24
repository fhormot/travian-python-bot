from Travian import Travian
from userData import *

import time

villages = ['01. Jo', '02. Joo']
attackTimes = [-1, -1]

fsVillage = ['13', '-83']

timeGap = 20

T = Travian(username, password, url_main_x3)
T.login()

while True:
    for index, village in enumerate(villages):
        T.switchVillage(village)

        attackSeconds = T.checkRaid(seconds=True)

        if not attackSeconds:
            attackTimes[index] = 9999
            continue
        else:
            attackTimes[index] = attackSeconds[0]

        # print(f'{village}[{len(attackSeconds)}]: {attackSeconds[0]}')

        if attackSeconds[0] <= timeGap-1:
            # Less than 9 seconds to attack
            try:
                T.buildArmy([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], max=True)
                T.quickFS(fsVillage, type=4, gapTime=timeGap/2)
            except:
                T.stop()

    minAttackTime = min(attackTimes)

    if minAttackTime > 60*2:
        time.sleep(60)
