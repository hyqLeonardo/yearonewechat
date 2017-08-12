# -*- coding: utf-8 -*-
# filename: show.py

import web


class Show(object):

    def GET(self):

        try:
            web_data = web.data()
            print("Acquire's Get webdata is ", web_data)   # 后台打日志
        except Exception as ex:
            print(ex)

        input_param = web.input()
        if len(input_param) == 0:
            print("no param in url")
            return "no input parameters found"

        # file path is set in url's param file, e.g ?file=./file/event/today_str/xxx.html
        html_file_path = input_param.file
        print('file path: {}'.format(html_file_path))

        with open(html_file_path, 'r') as file:
            html = file.read()

        return html

