# -*- coding: utf-8 -*-
# filename: handle.py

from yearonequant.util_quant import *
from yearonequant.event_object import *

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
            # media and text message type
            if isinstance(recMsg, receive.Msg):

                if recMsg.MsgType == "text":
                    text = recMsg.Content.decode('utf-8')
                    text = text.strip()

                    # push event list
                    if text[0] == 'E':
                        text = text.replace(' ', '')
                        event_name_chinese = text[1:]
                        event_name = EVENT_NAME_C2E.get(event_name_chinese)
                        if event_name:  # has this event
                            print('pushing event {}'.format(event_name))

                            today = datetime.datetime.now() - datetime.timedelta(days=1)
                            today_str = datetime2ymd_str(today)

                            file_path = './file/event/{}/{}.txt' \
                                .format(today_str, event_name)
                            html_path = './file/event/{}/{}.html' \
                                .format(today_str, event_name)

                            # read text file
                            with open(file_path) as file:
                                content = file.read()
                            # give a link to html page if list too long
                            if len(content) > 1000:
                                url = "http://139.224.234.82/wx/event/acquire?file={}" \
                                    .format(html_path)
                                hyper_link = "<a href=\"{}\">此链接</a>".format(url)
                                content = '因列表过长，只摘选部分事件，请点击{}查看完整列表。\n\n' \
                                          .format(hyper_link) + content
                                content = content[:1000]
                                content = content[:content.rfind('\n')] + '\n...\n'
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                            else:
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                        else:
                            content = '目前暂不支持事件{}，请尝试点击获取事件按钮。'\
                                .format(event_name_chinese)
                            replyMsg = reply.TextMsg(toUser, fromUser, content)

                    else:
                        content = "测试成功,可以正确处理文本消息"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)

                    return replyMsg.send()

                if recMsg.MsgType == "image":
                    mediaId = recMsg.MediaId
                    replyImageMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyImageMsg.send()

            # event message type
            if isinstance(recMsg, receive.EventMsg):

                if recMsg.Event == 'CLICK':
                    print("get click event")

                    if recMsg.EventKey == 'acquire_event':
                        event_names = '，'.join(EVENT_NAME_C2E.keys())
                        content = '回复 E+事件名称 可以获得近7日发生该事件的股票列表。\n' \
                                  '例如回复： E增持， 便可获得增持事件的列表。\n' \
                                  '目前支持的事件有{}'.format(event_names)
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()

                    if recMsg.EventKey == 'about_us':
                        print("handle about_us")
                        content = "YearOne(新晋元年)是一家创业中的量化对冲基金公司。" \
                                  "创始团队具有多年、多市场、多交易标的的投资经验，并以" \
                                  "最严格的合规性与职业道德准准则来要求自己，通过借助" \
                                  "交叉学科的力量持续创新，不停改进自己的投资方法。"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()

            print("暂不处理 {} 类型的请求".format(type(recMsg)))
            return reply.Msg().send()

        except Exception as Argument:
            print("exception: " + str(Argument))
            return Argument
