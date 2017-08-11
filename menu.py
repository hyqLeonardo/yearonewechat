# -*- coding: utf-8 -*-
# filename: menu.py
from urllib.request import urlopen
from basic import Basic


class Menu(object):

    def __init__(self):
        pass

    @staticmethod
    def create(postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, str):
            postData = postData.encode('utf-8')
        urlResp = urlopen(url=postUrl, data=postData)
        print(urlResp.read())

    @staticmethod
    def query(accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urlopen(url=postUrl)
        print(urlResp.read())

    @staticmethod
    def delete(accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urlopen(url=postUrl)
        print(urlResp.read())

    # 获取自定义菜单配置接口
    @staticmethod
    def get_current_selfmenu_info(accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = urlopen(url=postUrl)
        print(urlResp.read())


if __name__ == '__main__':

    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "name": "获取事件",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "增持",
                        "key":	"acquire_event_holding_increase"
                    },
                    {
                        "type": "click",
                        "name": "减持",
                        "key":	"acquire_event_holding_decrease"
                    },
                    {
                        "type": "click",
                        "name": "预增",
                        "key":	"acquire_event_forecast_growth"
                    },
                    {
                        "type": "click",
                        "name": "预减",
                        "key":	"acquire_event_forecast_decline"
                    }
                ]
            },
            {
                "type": "click",
                "name": "关于我们",
                "key":	"about_us"
            }
          ]
    }
    """
    accessToken = Basic().get_access_token()
    # myMenu.delete(accessToken)
    myMenu.create(postJson, accessToken)
