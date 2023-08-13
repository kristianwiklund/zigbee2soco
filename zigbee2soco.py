#!/usr/bin/python3

import sys 
import os

# debug code in case docker doesn't find the modules
#for path in sys.path:
#    print(path)


try:
    multiplier=int(os.environ.get("VOLUME_MULTIPLIER"))
except:
    multiplier=1

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


try:
    mqttuser=os.environ.get("MQTT_USER")
except:
    mqttuser=None
    
try:
    mqttpass=os.environ.get("MQTT_PASS")
except:
    mqttpass=None

    
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
            nv =  min(self.zones[speaker].volume+multiplier,100)
            self.zones[speaker].volume = nv

    def voldown(self, speaker):
        self.state = self.zones[speaker].get_current_transport_info()['current_transport_state']
        if self.state == "PLAYING":
            nv =  max(self.zones[speaker].volume-multiplier,0)
            self.zones[speaker].volume = nv

        

############## mqtt callbacks ########################

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, z2s, flags, rc):
    print("MQTT Connected with result code "+str(rc))
    if rc==4:
        print ("MQTT connection refused - bad username or password")
    elif rc==5:
        print("MQTT connection refused - not authorized")
        
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
        # both gen1 and gen2 have play_pause
        z2s.pause(topic)
    elif payload == "skip_forward" or payload == "track_next":
        # gen1 - skip_forward, gen2 - track_next
        z2s.skipforward(topic)
    elif payload == "rotate_right" or payload == "volume_up" or payload == "volume_up_hold":
        # gen1 - rotate, gen2 - volume...
        z2s.volup(topic)
    elif payload == "rotate_left"  or payload == "volume_down" or payload == "volume_down_hold": 
        # gen1 - rotate, gen2 - volume...
        z2s.voldown(topic)

    # not implemented:
    # dots buttons
    
    # skip_backward
    # skip_backward can be implemented by calling device_previous() but (in my experience) the wanted behavior is
    # to reset the currently playing tune to 0 at the first click, then, if the skip_backward is pressed again before
    # (a short time) has elapsed, we jump back one tune. This means that we need to get the play time, check it, then do something
    
        
################################

z2s = Z2S()
    
client = mqtt.Client(userdata=z2s)
if mqttuser:
    #print ("Using mqtt user name "+mqttuser+" / password '"+mqttpass+"'")
    client.username_pw_set(mqttuser, mqttpass)
client.on_connect = on_connect
client.on_message = on_message


    
print ("Connecting to "+mqtthost+":"+str(mqttport))
client.connect(mqtthost, int(mqttport), 60)

print ("zigbee2soco starting processing of events")

# mqtt loop
client.loop_forever()
