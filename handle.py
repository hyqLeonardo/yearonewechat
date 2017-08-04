# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "YearoneInvest"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update(''.join(list).encode('latin1'))
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except (Exception) as Argument:
            return Argument
