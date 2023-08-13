This connects sonos to zigbee2mqtt to control SONOS speakers with the IKEA SYMFONISK controllers - the rotary (gen1) and the new "flat" (gen2).
My rotary controllers are both dead - which means that the support for those need to be considered legacy, I will not be able to add features or fix bugs in a reliable way.



Tested with Sonos S1 - unknown if it works with S2.

The controller need to be named as the speaker, e.g. mqtt topic *prefix*/*speaker*, then everything works out of the box.
This is case sensitive and *prefix* need to uniquely identify what messages are from controllers. 

Easiest way to keep this running is with docker:
```docker-compose build && docker-compose up -d```

Configuration:
==============

You can either edit the config into the source, or if using docker-compose, change the environment variables in docker-compose.yml:

* PREFIX=zigbee/stereo _the zigbee mqtt prefix, as described above_
* MQTT_HOST=localhost  _mqtt host_
* MQTT_PORT=1883       _mqtt port_
* MQTT_USER=minion     _mqtt user_
* MQTT_PASS=banana     _mqtt password_
* VOLUME_MULTIPLIER=2  _higher number -> quicker reaction when turning the button_						  


Implemented:
============

* pause/restart - single click on button
* skip to next in playlist - double click on button
* volume control - might require the config above (debounce etc). The volume cannot be adjusted unless the speaker is playing something.


For those using Symfonisk Generation 1 - Rotary Controller
==========================================

You need to set debounce on the controller, see https://www.zigbee2mqtt.io/devices/E1744.html

I'm using this config for my controllers, cribbed directly from the zigbee2mqtt page linked above and saved here if it goes away for some reason:

```
    debounce: 0.1
    debounce_ignore:	
    - action
    - brightness
```


