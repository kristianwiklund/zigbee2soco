This connects sonos to zigbee2mqtt to control speakers with IKEA SYMFONISK controller

The controller need to be named after the speaker, e.g. mqtt topic <prefix>/<speaker>, then everything works out of the box.
This is case sensitive

<prefix> need to uniquely identify what messages are from controllers

You probably need to set debounce on the controller, see https://www.zigbee2mqtt.io/devices/E1744.html
