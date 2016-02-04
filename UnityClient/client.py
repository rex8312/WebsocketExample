# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gevent import monkey; monkey.patch_all()

import msgpack
import gevent
from ws4py.client.geventclient import WebSocketClient


def incoming(ws):
    while True:
        m = ws.receive()
        if m is not None:
            m = str(m)
            print(m, len(m))
            if len(m) == 35:
                ws.close()
                break
        else:
            break
    print("Connection closed!")


def outgoing(ws):
    for i in range(0, 40, 5):
        ws.send("*" * i)

    # We won't get this back
    ws.send("Foobar")

if __name__ == '__main__':
    ws = WebSocketClient('ws://127.0.0.1:8080/websocket', protocols=['http-only', 'chat'])
    ws.connect()

    for n in range(50):
        msg = msgpack.dumps(dict(msg="Hello world", no=n))
        ws.send(msg, binary=True)
        resp = str(ws.receive())
        print msgpack.loads(resp)
    ws.close()

    # greenlets = [
        # gevent.spawn(incoming, ws),
        # gevent.spawn(outgoing, ws),
    # ]
    # gevent.joinall(greenlets)
