#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TeletextApp.py
MIT License (c) Marie Faure <dev at faure dot systems>

TeletextApp extends GuizeroApp.
"""

from constants import *

import gettext

try:
    gettext.find("TeletextApp")
    traduction = gettext.translation('TeletextApp', localedir='locale', languages=['fr'])
    traduction.install()
except:
    _ = gettext.gettext  # cool, this hides PyLint warning Undefined name '_'

from GuizeroApp import GuizeroApp

import os, platform, sys, logging
from guizero import Text
from Sound import Sound


class TeletextApp(GuizeroApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        self.logger.info(_("Props started"))

        if platform.system() != 'Windows':
            if self.logger.level != logging.DEBUG:
                self._gui.full_screen = True  # exit fullscreen with Esc (so for props without a keyboard)
        else:
            self._gui.width = 592
            self._gui.height = 333

        self._gui.bg = 'black'
        self._gui.tk.config(cursor="none")

        self._texte = Text(self._gui, "")  # "" value is translated to "-" for MQTT_DISPLAY_TOPIC
        self._texte.height = 1080
        self._texte.text_color = 'green'
        self._texte.font = "Helvetica"

        if platform.system() != 'Windows':
            self._texte.size = "90"
        else:
            self._texte.size = "28"

        self._sound = Sound(self._logger)

        if platform.system() != 'Windows':
            os.system("amixer cset numid=3 1")  # audio jack
            os.system("amixer set 'PCM' -- -1000")

        if self._mqttConnected:
            try:
                (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, "-", qos=MQTT_DEFAULT_QoS, retain=True)
            except Exception as e:
                self._logger.error(
                    "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), "-", MQTT_DISPLAY_TOPIC))
                self._logger.debug(e)

    # __________________________________________________________________
    def onConnect(self, client, userdata, flags, rc):
        # extend as a virtual method
        # display message will '-' for black screen
        if hasattr(self, '_texte'):
            text = self._texte.value
            if not text:
                text = "-"
            try:
                (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, text, qos=MQTT_DEFAULT_QoS, retain=True)
            except Exception as e:
                self._logger.error(
                    "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), text, MQTT_DISPLAY_TOPIC))
                self._logger.debug(e)

    # __________________________________________________________________
    def onMessage(self, topic, message):
        # extend as a virtual method
        print(topic, message)
        if message in ["app:startup", "app:quit"]:
            super().onMessage(topic, message)
        elif message.startswith("afficher:"):
            text = message[9:]
            self._texte.value = text
            if self._mqttConnected:
                try:
                    (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, text, qos=MQTT_DEFAULT_QoS,
                                                             retain=True)
                    self._logger.info(
                        "{0} '{1}' (mid={2}) on {3}".format(_("Program sending message"), message, mid,
                                                            MQTT_DISPLAY_TOPIC))
                except Exception as e:
                    self._logger.error(
                        "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), message,
                                                  MQTT_DISPLAY_TOPIC))
                    self._logger.debug(e)
            self.publishMessage(self._mqttOutbox, "DONE " + message)
            self.publishDataChanges()
            self._sound.play('media/bell.wav')
        elif message.startswith("effacer"):
            self._texte.value = ""
            if self._mqttConnected:
                try:
                    (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, "-", qos=MQTT_DEFAULT_QoS, retain=True)
                    self._logger.info(
                        "{0} '{1}' (mid={2}) on {3}".format(_("Program sending message"), message, mid,
                                                            MQTT_DISPLAY_TOPIC))
                except Exception as e:
                    self._logger.error(
                        "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), message,
                                                  MQTT_DISPLAY_TOPIC))
                    self._logger.debug(e)
            self.publishMessage(self._mqttOutbox, "DONE " + message)
            self.publishDataChanges()
        else:
            self.publishMessage(self._mqttOutbox, "OMIT " + message)

    # __________________________________________________________________
    def publishAllData(self):
        super().publishAllData()

    # __________________________________________________________________
    def publishDataChanges(self):
        super().publishDataChanges()

    # __________________________________________________________________
    def quit(self):
        self._gui.exit_full_screen()
        self._gui.destroy()
        try:
            self._mqttClient.disconnect()
            self._mqttClient.loop_stop()
        except:
            pass
        self.logger.info(_("Props stopped"))
        sys.exit(0)
