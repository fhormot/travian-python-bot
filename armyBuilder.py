from Travian import Travian
from userData import *

import time
import random

T = Travian(username, password, url_main_x3)

T.login()
T.switchVillage('Jo')

while True:
    T.buildArmy([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], max=True)
    time.sleep(60*60)

# End
T.stop()
