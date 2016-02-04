# -*- coding: utf-8 -*-

from __future__ import print_function

from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket
from bottle import get
from bottle import run
from bottle import template
import msgpack


@get('/')
def index():
    return template('index')


@get('/websocket', apply=[websocket])
def echo(ws):
    while True:
        msg = ws.receive()
        if msg is not None:
            print('recv: {}'.format(msgpack.loads(msg)))
            ws.send(msg)
        else:
            break


if __name__ == '__main__':
    run(host='127.0.0.1', port=8080, server=GeventWebSocketServer)