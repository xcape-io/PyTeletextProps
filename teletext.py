#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teletext.py
MIT License (c) Marie Faure <dev at faure dot systems>

Displays message received from MQTT server in fullscreen on main monitor and play a sound.

To switch MQTT broker, kill the program and start again with new arguments.
Use -d option to start in windowed mode instead of fullscreen.

usage: python3 teletext.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
 -h, --help   show this help message and exit
 -s SERVER, --server SERVER
      change MQTT server host
 -p PORT, --port PORT change MQTT server port
 -d, --debug   set DEBUG log level
 -l LOGGER, --logger LOGGER
      use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
"""

import paho.mqtt.client as mqtt
import os, sys, uuid

from constants import *
from TeletextApp import TeletextApp
from Singleton import Singleton, SingletonException


me = None
try:
    me = Singleton()
except SingletonException:
    sys.exit(-1)
except BaseException as e:
    print(e)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# translation
import gettext

try:
    gettext.find(APPLICATION)
    traduction = gettext.translation(APPLICATION, localedir='locale', languages=['fr'])
    traduction.install()
except:
    _ = gettext.gettext  # cool, this hides PyLint warning Undefined name '_'

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = TeletextApp(sys.argv, mqtt_client, debugging_mqtt=False)

# guizero event loop
app.loop()

del me

sys.exit(0)
