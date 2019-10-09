# Room 2.0 Outbox protocol
***An effective protocol for MQTT messages sent by connected props for Escape Room.***

Connected props for Escape Room exchange data and messages with a MQTT broker.

Room 2.0 Outbox protocol is a minimal implementation to structure messages sent by connected props. 

However props may use MQTT topics in any way, for example [Teletext Props](https://github.com/fauresystems/TeletextProps) publishes its displayed text as a *retained* message in a dedicated MQTT topic.

## Outbox
Room 2.0 Outbox protocol defines messages sent in props outbox, which is a MQTT topic structured like this:
```python
Room/Name of the room/Props/Name of the props/outbox
```
For example:
```python
Room/Demoniak/Props/Raspberry Teletext/outbox
```

## Inbox
The props also subscribes to its dedicated inbox topic to listen to command such as actuators:
```python
Room/Name of the room/Props/Name of the props/inbox
```
For example:
```python
Room/Demoniak/Props/Raspberry Teletext/inbox
```

## Protocol for outbox
The protocol has been defined to be **human readable** (so debugging Escape Room is easy) and  **simple to parse** (so low-end MCU can parse it quickly, such as Arduino):

* `CONNECTED` is sent when the props is connected to the MQTT broker
* `DISCONNECTED` is set as the MQTT *will* for the outbox topic
* `DATA var1=value1 var2=value2` to report sensors or puzzle game state
* `REQU command` to send a request to another props
* `PROG command` to send a program request to the Escape Game controller (Room 2.0)
* `DONE command` to report command has been received and done
* `OMIT command` to report unsupported command has been received
* `OVER command` to report an Escape Game challenge has been complete
* `MESG any interesting stuff to report`


## Author

**Marie FAURE** (Oct 9th, 2019)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://www.live-escape.net/" target="_blank">Live Escape Grenoble</a>