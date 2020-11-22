This connects sonos to zigbee2mqtt to control SONOS speakers with IKEA SYMFONISK controller

The controller need to be named after the speaker, e.g. mqtt topic *prefix*/*speaker*, then everything works out of the box.
This is case sensitive and *prefix* need to uniquely identify what messages are from controllers

You probably need to set debounce on the controller, see https://www.zigbee2mqtt.io/devices/E1744.html

I'm using this config for my controllers, cribbed directly from the zigbee2mqtt page linked above and saved here if it goes away for some reason:

```
    debounce: 0.1
    debounce_ignore:	
    - action
    - brightness
```

I'm basically done with this now, will likely not add the skip backwards (triple click) functionality.

Easiest way to keep this running is with docker:
```docker-compose build && docker-compose up -d```


Implemented:
============

* pause/restart - single click on button
* skip to next in playlist - double click on button
* volume control - might require the config above (debounce etc)
