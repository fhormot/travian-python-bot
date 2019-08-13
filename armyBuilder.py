from Travian import Travian
from userData import *

import time
import random

T = Travian(username, password, url_main_x3)

T.login()
# T.checkBuildingAvailability('26')
# T.sendArmy([12, -61], [0, 0, 27, 0, 0, 0, 0, 0, 0, 0, 1], 4)
# T.sendArmy([12, -61], [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 4)
# T.sendArmy([12, -61], [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 4)

while True:
    T.switchVillage('Honey')
    T.buildArmy([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], max=True)

    time.sleep(random.uniform(0.1, 0.2)*60)

    T.switchVillage('Nibiru')
    T.buildArmy([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], max=True)
    T.sendArmy([8, -90], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 2)

    time.sleep(random.uniform(0.7, 1.5)*60)

# End
T.stop()
