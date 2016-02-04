#-*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from bottle import run
from bottle import get
from bottle import template
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket


users = set()


@get('/')
def index():
    return template('index')


@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in users:
                u.send(msg)
        else:
            break
    users.remove(ws)


if __name__ == '__main__':
    run(host='127.0.0.1', port=8080, server=GeventWebSocketServer)