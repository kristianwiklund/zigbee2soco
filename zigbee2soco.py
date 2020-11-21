#!/usr/bin/python3

import sys 

for path in sys.path:
    print(path)

#change this to fit your own prefix. I use the stereo part to automatically identify only stereo events

mqttprefix="zigbee/stereo"

import paho.mqtt.client as mqtt
import soco
import traceback

def discover():
    zones = {x.player_name:x for x in  soco.discover()}
    
    #print("ZONES: "+str(zones))
    return zones

def pause(zones, speaker):
    print("Pausing "+speaker)
    state = zones[speaker].get_current_transport_info()['current_transport_state']
    #print(state)

    if state == "PLAYING":
        zones[speaker].pause()
    else:
        zones[speaker].play()

def skipforward(zones, speaker):
    print("Pausing "+speaker)
    state = zones[speaker].get_current_transport_info()['current_transport_state']
    #print(state)

    zones[speaker].next()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqttprefix+"/+/action")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, zones, msg):
    
    print(msg.topic+" "+str(msg.payload))
    
    payload = msg.payload.decode("utf-8")
    print(payload)

    try:
        topic = msg.topic
        topic = topic.replace(mqttprefix+"/","")
        topic = topic.replace("/action","")
        #print(topic)
        #print(zones)
#    .removesuffix("/action")
    except:
        print(traceback.format_exc())
        print (sys.exc_info()[0])


    if not topic in zones:
        print("No such speaker: "+topic)
        return

    if payload == "play_pause":
        pause(zones, topic)
    elif payload == "skip_forward":
        skipforward(zones, topic)
        
## do stuff

zones = discover()
    
client = mqtt.Client(userdata=zones)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
