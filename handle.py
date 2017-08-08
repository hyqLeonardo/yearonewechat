# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import reply
import receive
import web

class Handle(object):

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)   #后台打日志
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
                    content = "测试成功,可以正确处理图片消息，返回接受到的图片"
                    replyTextMsg = reply.TextMsg(toUser, fromUser, content)
                    replyImageMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    # return replyTextMsg.send(), replyImageMsg.send() # can't reply 2 message
                    return replyImageMsg.send()

            if isinstance(recMsg, receive.EventMsg):

                if recMsg.Event == 'CLICK':
                    print("get click event")
                    if recMsg.EventKey == 'about_us':
                        print("handle about us")
                        content = "YearOne（新晋元年）是一家创业中的量化对冲基金公司。" \
                                  "创始团队具有多年、多市场、多交易标的的投资经验，并以" \
                                  "最严格的合规性与职业道德准准则来要求自己，通过借助" \
                                  "交叉学科的力量持续创新，不停改进自己的投资方法。"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()

            print("暂且不处理")
            return reply.Msg().send()

        except (Exception) as Argument:
            print("exception: " + str(Argument))
            return Argument
