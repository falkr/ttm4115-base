from sense_hat import SenseHat
import time
import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("action/state")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    set_color(msg.payload)

# Sets the color on the Sense Hat
def set_color(payload):
    sense = SenseHat()
    message = payload.decode('utf-8')
    new_color = json.loads(message).get("color")
    color_dict= {
        'red': (255,0,0),
        'green': (0,255,0),
        'none': (0,0,0)
        }

    for i in range(8):
      for j in range(8):
          sense.set_pixel(i,j, color_dict.get(new_color))

# ONLY USED FOR WHEN THERE IS NO SENSE HAT IN THE PICTURE/TESTING
def set_fake_color(payload):
    message = payload.decode('utf-8')
    new_color = json.loads(message).get("color")

    colors = {
        'red':'Red',
        'green':'Green',
        'none':'None'
        }

    print("Color is now " + colors.get(new_color))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 120)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
