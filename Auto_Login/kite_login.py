from kiteconnect import KiteConnect
import urllib.parse
from requests import auth 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, time
from os.path import expanduser
from selenium.webdriver.chrome.options import Options

from datetime import datetime

import pdb
import sys
import hmac, base64, struct, hashlib, time
import logging

from config import CHROME_VERSION, KITE_LOGIN_URL
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore


class Kite_Login:

    def __init__(self,zerodha_cred):
        self.zerodha_cred = zerodha_cred

    def get_hotp_token(self,secret, intervals_no):
        key = base64.b32decode(secret, True)
        msg = struct.pack(">Q", intervals_no)
        h = hmac.new(key, msg, hashlib.sha1).digest()
        o = h[19] & 15
        h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
        return h

    def get_totp_token(self,secret):
        totp = str(self.get_hotp_token(secret, intervals_no=int(time.time())//30))
        if len(totp) < 6:
            totp = '0' + totp
        return totp
    
    def web_login(self,_client):
    
        user_id = self.zerodha_cred[_client]['user_id']
        password = self.zerodha_cred[_client]['password']
        api_key = self.zerodha_cred[_client]['api_key']
        auth_key = self.zerodha_cred[_client]['auth_key']

        # kite = KiteConnect(api_key=api_key)
        
                
        url  = KITE_LOGIN_URL + api_key 
        
        try:
            chrome_path = os.path.join( os.path.dirname( os.getcwd() ) , 'external_files', CHROME_VERSION)
            options = Options()
            options.add_argument('--headless') #for headless
            driver = webdriver.Chrome(chrome_path, options=options)

            driver.get(url)

            time.sleep(2)
            input_fields = driver.find_elements_by_tag_name('input')
            logging.info("Sending Username")
            input_fields[0].send_keys(user_id)
            logging.info("Sending Password")
            input_fields[1].send_keys(password)
            input_fields[1].send_keys(Keys.ENTER)
            time.sleep(1)
            
            #Next Page
            two_fa = driver.find_elements_by_tag_name('input')
            common_ans = self.get_totp_token(auth_key)
            two_fa[0].send_keys(str(common_ans))
            two_fa[0].send_keys(Keys.ENTER)
            time.sleep(1)
            
            logging.info(common_ans)
            

            logging.info(driver.current_url)
            while("request_token=" not in driver.current_url):
                logging.info (driver.current_url)
                driver.save_screenshot('login.png')
                time.sleep(3)

            redirect_url = driver.current_url
            logging.info(f'redirectURL-{redirect_url}')
            parsed = urllib.parse.urlparse(redirect_url)
            query_dict = dict(urllib.parse.parse_qsl(parsed.query))
            request_token = query_dict['request_token']
            logging.info(f'req token-{request_token}')
            driver.close
            return request_token
        except Exception as e:
            logging.info (e)
            logging.info('closing')
            driver.close()














