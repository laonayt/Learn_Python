#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

s = socket.socket()
s.bind(socket.gethostname(),8080)
s.listen()
while True:
    c.addr