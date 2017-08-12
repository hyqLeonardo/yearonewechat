# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
from show import Show

urls = (
    '/wx', 'Handle',
    '/wx/event/acquire', 'Show'
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
