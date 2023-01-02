import os
import pathlib
import sys
import logging
from utils.read_yaml import gen_json
from kiteconnect import KiteConnect
from kite_login import Kite_Login
from datetime import datetime, timedelta
from config import YML_PATH, ist_time, LOG_FILE_NAME, CUR_DATE

logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE_NAME, filemode="a+",
                        format="%(asctime)-12s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logging.Formatter.converter = ist_time

class Gen_Acc_Token:
    def gen_acc_token(self):
        
        user_creds = gen_json(YML_PATH,"config_zerodha.yml")
        gen_login = Kite_Login(user_creds)
        auth_keys={}
        

        for user in user_creds:
            _token = gen_login.web_login(user)
            kite = KiteConnect(api_key=user_creds[user]['api_key'] )
            data = kite.generate_session(_token, api_secret=user_creds[user]['api_secret'])
            access_token=data["access_token"]
            
            logging.info(_token)
            file_path = os.path.join( os.path.dirname( os.getcwd() ) , 'auth_files')
            auth_file = open( os.join( file_path, user+"_auth.txt","w") )
            auth_file.write(access_token) 
            auth_file.close()
            auth_keys[user] = access_token

            auth_keys['date'] = CUR_DATE

            logging.info(auth_keys)

