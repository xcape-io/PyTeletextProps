# Teletext connected props
***Display messages received from MQTT server on fullscreen main monitor.***

TeletextProps is pure python application to build a Raspberry connected props for Escape Room. Ring a bell and turn on a light. 


## MqttApp and MqttVar base class
TeletextApp extends *MqttApp*, the asynchronous (*asyncio*) python base app for Raspberry connected props.

*Python script hangs* have been reported when `paho-mqtt` is running asynchronously with QoS 2 on a network with significant packet loss (most of Wifi networks).

We have choosen MQTT QoS 1 as default (see *constants.py*).

MQTT topics are defined in *definitions.ini*.

PubSub variables extend *MqttVar*, it is an helper to track value changes and to optimize publishing values in MQTT topic outbox.

You might not modify these files.


## GuizeroApp base class
GUI is built with *<a href="https://lawsie.github.io/guizero/" target="_blank">guizero</a>* library.

Extend this base class to build a connected props which does simple text display (for visual effects and ttf font, see TelefxProps), sound playback and GPIO stuff.

You might not modify this file.


## TeletextApp
Teletext props is built with the following files:
* teletext.py
* constants.py
* definitions.ini
* logging.ini
* TeletextApp.py

Use TeletextApp as a model to create your own connected props which does simple text display, sound playback and GPIO stuff.


## Installation
Download `TeletextProps-master.zip` from this GitHub repository and unflate it on your Raspberry Pi.

Edit `definitions.ini` to set MQTT topics for your Escape Room:
```python
[mqtt]
; mqtt-sub-* and app-inbox topics are subscribed by MqttApp
app-inbox = Room/Demoniak/Props/Raspberry Teletext/inbox
app-outbox = Room/Demoniak/Props/Raspberry Teletext/outbox
mqtt-sub-room-scenario = Room/Demoniak/Control/game:scenario
``` 


## Other python frameworks for connected props
At <a href="https://www.live-escape.net/" target="_blank">Live Escape Grenoble</a> we engineered othe props with other frameworks for other needs:

* PyGame props
    - Tetris hacked
    - mechanic Piano sound player
    - hacker intrusion puzzle
* PyQt5 props
    - fortune telling table (alphanum LED switching)
    - electric jack cylinder control
* Kivy props
    - teletext with visual effects
    
You may follow on our <a href="https://github.com/fauresystems?tab=repositories" target="_blank">GitHub repositories</a>, props source code is planned to be published in year 2020.


## Author

**Marie FAURE** (Oct 1th, 2019)
* company: FAURE SYSTEMS SAS
* mail: <a href="mailto:dev@faure.systems" target="_blank">dev@faure.systems</a>
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://www.live-escape.net/" target="_blank">Live Escape Grenoble</a>