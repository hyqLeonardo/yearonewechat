# -*- coding: utf-8 -*-
# filename: basic.py
from urllib.request import urlopen
import time
import json

class Basic:

    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):

        appId = "wxb6c1126cee0cb7a6"
        appSecret = "4bcf6c3e704f7f27af33f53daab5bc66"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))

        urlResp = urlopen(postUrl)
        urlResp = json.loads(urlResp.read().decode('utf-8'))
        
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self):

        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):

        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()

