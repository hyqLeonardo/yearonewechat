# -*- coding: utf-8 -*-
# filename: handle.py

from yearonequant.util_quant import *

import reply
import receive
import web


class Handle(object):

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)   # 后台打日志
            recMsg = receive.parse_xml(webData)

            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName

            if isinstance(recMsg, receive.Msg):

                if recMsg.MsgType == "text":
                    content = "测试成功,可以正确处理文本消息"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()

                if recMsg.MsgType == "image":
                    mediaId = recMsg.MediaId
                    replyImageMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyImageMsg.send()

            if isinstance(recMsg, receive.EventMsg):

                if recMsg.Event == 'CLICK':
                    print("get click event")

                    if recMsg.EventKey == 'about_us':
                        print("handle about_us")
                        content = "YearOne(新晋元年)是一家创业中的量化对冲基金公司。" \
                                  "创始团队具有多年、多市场、多交易标的的投资经验，并以" \
                                  "最严格的合规性与职业道德准准则来要求自己，通过借助" \
                                  "交叉学科的力量持续创新，不停改进自己的投资方法。"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()

                    if 'acquire_event_' in recMsg.EventKey:

                        today = datetime.datetime.now() - datetime.timedelta(days=1)
                        today_str = datetime2ymd_str(today)
                        event_name = recMsg.EventKey[14:]   # get event name
                        print('pushing event {}'.format(event_name))

                        file_path = './file/event/{}/{}.txt'\
                            .format(today_str, event_name)
                        html_path = './file/event/{}/{}.html'\
                            .format(today_str, event_name)

                        with open(file_path) as file:
                            content = file.read()
                        # give a link to html page if list too long
                        if len(content) > 1000:
                            url = "http://139.224.234.82/wx/event/acquire?file={}"\
                                .format(html_path)
                            hyper_link = "<a href=\"{}\">此链接</a>".format(url)
                            content = '因列表过长，只摘选部分事件，请点击{}查看完整列表。\n\n'\
                                .format(hyper_link) + content
                            replyMsg = reply.TextMsg(toUser, fromUser, content[:1000])
                        else:
                            replyMsg = reply.TextMsg(toUser, fromUser, content)

                        return replyMsg.send()

            print("暂不处理 {} 类型的请求".format(type(recMsg)))
            return reply.Msg().send()

        except Exception as Argument:
            print("exception: " + str(Argument))
            return Argument
