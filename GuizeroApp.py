#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GuizeroApp.py
MIT License (c) Marie Faure <dev at faure dot systems>
GuizeroApp extends MqttApp.
"""

from constants import *

import gettext
import os, platform, signal, yaml

try:
    gettext.find("GuizeroApp")
    traduction = gettext.translation('GuizeroApp', localedir='locale', languages=['fr'])
    traduction.install()
except:
    _ = gettext.gettext  # cool, this hides PyLint warning Undefined name '_'

from MqttApp import MqttApp
from guizero import App

import sys


class GuizeroApp(MqttApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        self._gui = App(APPLICATION_GUI_NAME)

        self._relaunched = False

        if platform.system() != 'Windows':
            signal.signal(signal.SIGUSR1, self.receiveSignal)

        self._gui.tk.after(500, self.poll)

    # __________________________________________________________________
    def loop(self):
        # guizero loop
        self._gui.display()

    # __________________________________________________________________
    def onDisconnect(self, client, userdata, rc):
        # extend as a virtual method
        if self._relaunched:
            self._relaunched = False
            try:
                self._mqttClient.connect_async(self._mqttServerHost, port=self._mqttServerPort, keepalive=MQTT_KEEPALIVE)
            except Exception as e:
                self._logger.error(_("MQTT API : failed to call connect_async()"))
                self._logger.debug(e)

    # __________________________________________________________________
    def onMessage(self, topic, message):
        # extend as a virtual method
        print(topic, message)
        if message == "app:startup":
            self.publishAllData()
            self.publishMessage(self._mqttOutbox, "DONE " + message)
        elif message == "app:quit":
            self.publishAllData()
            self.publishMessage(self._mqttOutbox, "DONE " + message)
            self.quit()
        else:
            self.publishMessage(self._mqttOutbox, "OMIT " + message)

    # __________________________________________________________________
    def poll(self):
        # required for Tkinter tn cathc signal quickly
        self._gui.tk.after(500, self.poll)

    # __________________________________________________________________
    def quit(self):
        self._gui.exit_full_screen()
        self._gui.destroy()
        try:
            self._mqttClient.disconnect()
            self._mqttClient.loop_stop()
        except:
            pass
        self.logger.info(_("Program done"))
        sys.exit(0)

    # __________________________________________________________________
    def receiveSignal(self, signalNumber, frame):
        if signalNumber == signal.SIGUSR1:
            self.relaunch()

    # __________________________________________________________________
    def relaunch(self):
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as conffile:
                self._config = yaml.load(conffile, Loader=yaml.SafeLoader)
        print(self._config)
        if 'host' in self._config:
            self._mqttServerHost = self._config['host']
        if 'port' in self._config:
            self._mqttServerPort = self._config['port']
        self._relaunched = True
        self._mqttClient.disconnect()
        try:
            self._mqttClient.connect_async(self._mqttServerHost, port=self._mqttServerPort, keepalive=MQTT_KEEPALIVE)
        except Exception as e:
            self._logger.error(_("MQTT API : failed to call connect_async()"))
            self._logger.debug(e)

