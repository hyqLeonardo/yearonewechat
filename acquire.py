# -*- coding: utf-8 -*-
# filename: handle.py

import web


class Acquire(object):

    def GET(self):

        data = web.input()
        if len(data) == 0:
            return "hello, no data found"

        # file path is set in url's param file, e.g ?file=./file/event/today_str/xxx.html
        html_file_path = data.file

        with open(html_file_path, 'r') as file:
            html = file.read()

        return html

