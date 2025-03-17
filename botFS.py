from Travian import Travian
from userData import *

import time
import random

from pprint import pprint

def main():
    T = Travian(username, password, url_main)

    try:
        T.login()

        ids = T.id_matcher()
        pprint(ids)

        T.stop()
        exit()
        
        buildings = [
            'Main Building',
            'Warehouse',
            'Granary',
            'City Wall',
            'Barracks',
            'Heromansion',
            'Academy',
            'Smithy',
            'Stable',
            'Brickyard',
            'Sawmill',
            'Ironfoundry',
            'Grainmill',
        ]

        # for building in buildings:
        #     ret_val = T.build_new_building(building)
        #     print(f'Building {building} - {ret_val}')

        T.max_buildings(buildings)
        # time.sleep(60)

        T.stop()
        exit()
    except Exception as e:
        print(e)

        T.stop()
        exit()

if __name__ == '__main__':
    main()