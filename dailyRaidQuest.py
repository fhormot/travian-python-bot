from Travian import Travian
from userData import *

import time
import random

T = Travian(username, password, url_main)

T.login()
# T.checkBuildingAvailability('26')
T.sendArmy([12, -61], [22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 4)
T.sendArmy([12, -61], [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 4)
T.sendArmy([12, -61], [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 4)

T.sendArmy([15, -61], [0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 1], 4)
T.sendArmy([15, -61], [0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 1], 4)
T.sendArmy([15, -61], [0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1], 4)

# End
T.stop()
