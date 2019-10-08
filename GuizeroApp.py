#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GuizeroApp.py
MIT License (c) Marie Faure <dev at faure dot systems>
GuizeroApp extends MqttApp.
"""

from constants import *

import gettext
try:
	gettext.find("GuizeroApp")
	traduction = gettext.translation('GuizeroApp', localedir='locale', languages=['fr'])
	traduction.install()
except:
	_ = gettext.gettext # cool, this hides PyLint warning Undefined name '_'

from MqttApp import MqttApp
from guizero import App

import sys


class GuizeroApp(MqttApp):

	#__________________________________________________________________
	def __init__(self, argv, client, debugging_mqtt=False):
		
		super().__init__(argv, client, debugging_mqtt)

		self._gui = App(APPLICATION_GUI_NAME)

	# __________________________________________________________________
	def loop(self):
		# guizero loop
		self._gui.display()

	#__________________________________________________________________
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
