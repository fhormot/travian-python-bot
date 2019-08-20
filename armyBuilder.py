from Travian import Travian
from userData import *

import time
import random

T = Travian(username, password, url_main_x3)

T.login()

T.switchVillage('Jo')
T.buildArmy([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], max=True)

# End
T.stop()
