#!/usr/bin/python3

import sys 
import os

# debug code in case docker doesn't find the modules
#for path in sys.path:
#    print(path)



try:
    mqttprefix=os.environ.get("PREFIX")
except:
    mqttprefix="zigbee/stereo"

try:
    mqtthost=os.environ.get("MQTT_HOST")
except:
    mqtthost="localhost"

try:
    mqttport=os.environ.get("MQTT_PORT")
except:
    mqttport=1883


    
import paho.mqtt.client as mqtt
import soco
import traceback



# class, to keep some "globals" contained

class Z2S:

    def __init__(self):
        self.discover()
        
    def discover(self):
        self.zones = {x.player_name:x for x in  soco.discover()}
        
        print("ZONES: "+str(self.zones))
        return self.zones

    def pause(self, speaker):
        self.state = self.zones[speaker].get_current_transport_info()['current_transport_state']
        #priant(state)

        if self.state == "PLAYING":
            print("Pause "+speaker)
            self.zones[speaker].pause()
        
        else:
            print("Play "+speaker)
            self.zones[speaker].play()

    def skipforward(self, speaker):
        print("skip forward "+speaker)

        self.zones[speaker].next()

    def volup(self, speaker):
        self.state = self.zones[speaker].get_current_transport_info()['current_transport_state']
        if self.state == "PLAYING":
            self.zones[speaker].volume+=1

    def voldown(self, speaker):
        self.state = self.zones[speaker].get_current_transport_info()['current_transport_state']
        if self.state == "PLAYING":
            self.zones[speaker].volume-=1
        

############## mqtt callbacks ########################

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, z2s, flags, rc):
    print("MQTT Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqttprefix+"/+/action")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, z2s, msg):

    print(msg.topic+" "+str(msg.payload))
    
    payload = msg.payload.decode("utf-8")

    try:
        topic = msg.topic
        topic = topic.replace(mqttprefix+"/","")
        topic = topic.replace("/action","")
        #print(topic)
        #print(zones)

    except:
        print(traceback.format_exc())
        print (sys.exc_info()[0])


    # move this to the object
    if not topic in z2s.zones:
        print("No such speaker "+topic+" running discover")
        z2s.discover()

        if not topic in z2s.zones:
            print ("Not found after rescan")
            return

    if payload == "play_pause":
        z2s.pause(topic)
    elif payload == "skip_forward":
        z2s.skipforward(topic)
    elif payload == "rotate_right":
        z2s.volup(topic)
    elif payload == "rotate_left":
        z2s.voldown(topic)
        
################################

z2s = Z2S()
    
client = mqtt.Client(userdata=z2s)
client.on_connect = on_connect
client.on_message = on_message

print ("Connecting to "+mqtthost+":"+str(mqttport))
client.connect(mqtthost, int(mqttport), 60)

print ("zigbee2soco starting processing of events")

# mqtt loop
client.loop_forever()
