# Teletext connected props
***Display messages with Raspberry connected props for Escape Room.***

[Teletext Props](https://github.com/fauresystems/PyTeletextProps) is pure python application to build a Raspberry connected props for Escape Room. 

This props listen to MQTT messages to display a text on a display monitor, ring a bell and turn on a light. Messages and commands are sent remotely from anywhere (no more need of long HDMI cables in Escape Rooms).

This props is inspired from a Water Well props created for [Live Escape Grenoble](https://www.live-escape.net/) rooms, controlled with **Room** software, this props can be controlled with [Teletext Plugin](https://github.com/fauresystems/TeletextPlugin) or any application able to publish MQTT messages.

The Water Well props was based on <a href="https://kivy.org/" target="_blank">Python Kivi</a> to get water waves visual effects. 

This props based on <a href="https://lawsie.github.io/guizero/start/" target="_blank">Guizero</a> is a very good start to code a very first GUI props on Raspberry. Create your own connected props, you just have to hack the code in `TeletextApp.py` file.

You will find <a href="https://xcape.io/public/documentation/en/room/AddaRaspberrypropsTeletext.html" target="_blank">detailed installation help in the Room manual</a>.


## Installation
Download `PyTeletextProps-master.zip` from this GitHub repository and unflate it on your Raspberry Pi.

Install dependencies
```bash
pip3 install -r requirements.txt
```

Edit `definitions.ini` to set MQTT topics for your Escape Room:
```python
[mqtt]
; mqtt-sub-* and app-inbox topics are subscribed by MqttApp
app-inbox = Room/My room/Props/Raspberry Teletext/inbox
app-outbox = Room/My room/Props/Raspberry Teletext/outbox
mqtt-sub-room-scenario = Room/My room/Control/game:scenario
``` 


## Usage
Start `teletext.py` script:

```bash
usage: python3 teletext.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
 -h, --help   show this help message and exit
 -s SERVER, --server SERVER
      change MQTT server host
 -p PORT, --port PORT change MQTT server port
 -d, --debug   set DEBUG log level
 -l LOGGER, --logger LOGGER
      use logging config file
```

To switch MQTT broker, kill the program and start again with new arguments.


## Understanding the code

### *TeletextApp*
Teletext props is built with the following files:
* `teletext.py` main script to start the props
* `constants.py`
* `definitions.ini`
* `logging.ini`
* __`TeletextApp.py`__ props related code

It depends on:
* `GuizeroApp.py` base class to create a guizero event loop
* `MqttApp.py` base class to publish/subscribe MQTT messages
* `MqttVar.ini` base class to optimize network communications
* `Singleton.ini` to ensure one instance of application is running
* `Sound.py` simple *aplay* wrapper

Use ***TeletextApp*** as a model to create your own connected props if you need simple text display, sound playback. You can also add GPIO stuff.

About `create-teletextprops-tgz.bat`:
* install <a href="https://www.7-zip.org/" target="_blank">7-Zip</a> on your Windows desktop
* run `create-teletextprops-tgz.bat` to archive versions of your work

#### MQTT message protocol:
> This props has been created for [Live Escape Grenoble](https://www.live-escape.net/) rooms, controlled with **Room** software so MQTT messages published in the props outbox implement the <a href="https://github.com/fauresystems/TeletextProps/blob/master/PROTOCOL.md" target="_blank">Room Outbox protocol</a>.

#### IDE for hacking `TeletextApp.py`:
> You can open a PyCharm Professional project to hack the code remotely, thanks to `.idea` folder. Or if you prefer to the code hack directly on the Raspberry, we suggest <a href="https://eric-ide.python-projects.org/" target="_blank">Eric6 IDE</a>. 


### *GuizeroApp* base class
*TeletextApp* extends *GuizeroApp*, python base app for Raspberry connected props which require simple text display. 

For more advanced text display (visual effects, True-Type fonts) you may see *Kivi* props below such as TelefxProps.

GUI is built with *<a href="https://lawsie.github.io/guizero/" target="_blank">guizero</a>* library. If you don't need display, prefer *Asyncio* props.

Extend this base class to build a connected props which does simple text display, sound playback. Optionally you can GPIO stuff.

You might not modify `GuizeroApp.py` file.


### *MqttApp* and *MqttVar* base classes
*GuizeroApp* extends *MqttApp*, the python base app for Raspberry connected props.


MQTT topics are defined in *definitions.ini*.

PubSub variables extend *MqttVar*, it is an helper to track value changes and to optimize publishing values in MQTT topic outbox.

You might not modify `MqttApp.py` an `MqttVar.py` files.

#### Notes about MQTT QoS:
>*Python script hangs* have been reported when `paho-mqtt` is running asynchronously with QoS 2 on a network with significant packet loss (particularly Wifi networks).

We have choosen MQTT QoS 1 as default (see *constants.py*).


## Other python frameworks for connected props
At <a href="https://faure.systems/" target="_blank">Faure Systems</a> we engineered connected props with several frameworks for many different needs:

* *Asyncio* props
    - game automation
    - relay box control (room electricity and doors)
    - GPIO only automation
* *PyGame* props
    - Tetris hacked
    - mechanic Piano sound player
    - hacker intrusion puzzle
* *PyQt5* props
    - fortune telling table (alphanum LED switching)
    - electric jack cylinder control
* *Guizero* props
    - teletext
* *Kivy* props
    - teletext with visual effects
    
You may follow on our <a href="https://github.com/fauresystems?tab=repositories" target="_blank">GitHub repositories</a>, props source code is planned to be published in year 2020.


## Author

**Marie FAURE** (Oct 9th, 2019)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>