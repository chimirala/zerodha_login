
'''
    contains config details used in  project 
'''

import pathlib
from datetime import datetime, timedelta

CHROME_VERSION = "chromedriver108.exe"  #provide exe name used for chrome
KITE_LOGIN_URL =  "https://kite.trade/connect/login?v=3&api_key="  # url used for login to kite. GIven in API
YML_PATH = pathlib.Path(__file__).parent.resolve()  # used to link yml config and generate log in same folder

CUR_DATE=datetime.now().strftime("%y_%m_%d") 
LOG_FILE_NAME = YML_PATH + str(CUR_DATE) + ".log"  

def ist_time(sec, what):
    '''sec and what is unused.'''
    _curr_time = datetime.now() + timedelta(hours=5, minutes=30)
    return _curr_time.timetuple()

