# -*- coding: utf-8 -*-
# filename: media.py
from basic import Basic
import requests


class Media(object):

    def __init__(self):
        pass

    # 上传图片
    def uplaod(self, accessToken, filePath, mediaType):

        openFile = open(filePath, "rb")

        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (accessToken, mediaType)
        urlResp = requests.post(postUrl, files={'media': openFile})
        print(urlResp)

if __name__ == '__main__':

    myMedia = Media()
    accessToken = Basic().get_access_token()
    filePath = "./file/event/test.jpg"
    mediaType = "image"
    myMedia.uplaod(accessToken, filePath, mediaType)

