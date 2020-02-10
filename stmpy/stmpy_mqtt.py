from stmpy import Machine, Driver
import paho.mqtt.client as mqtt
import logging
import json

scheduler = Driver()

class Lights:

    busy = False

    def __init__(self):
        Lights.busy = False
        self.responsetopic = "action/state"

    def on_init(self):
        print('None!')
        Lights.busy = False

    def on_red(self):
        print('Red Light')
        Lights.busy = True
        Lights.MQTT.client.publish(self.responsetopic, payload=json.dumps({ "color" : "red"}), qos=0, retain=False)
        self.stm.start_timer('goto_none', 3000)

    def on_green(self):
        print('Green Light')
        Lights.busy = True
        print("Sending green")
        Lights.MQTT.client.publish(self.responsetopic, payload=json.dumps({ "color" : "green"}), qos=0, retain=False)
        self.stm.start_timer('goto_none', 3000)

    def on_none(self):
        print('None!')
        Lights.busy = False
        Lights.MQTT.client.publish(self.responsetopic, payload=json.dumps({ "color" : "none"}), qos=0, retain=False)


class MQTT:

    scheduler = None

    def __init__(self, scheduler):

        Lights.MQTT = self
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        MQTT.scheduler= scheduler
        self.client.loop_start()


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe("results/checkCredentials")
        self.client.subscribe("commands/checkAvailable")


    def on_message(self, client, userdata, msg):

        message = json.loads(msg.payload)
        topic = msg.topic

        if topic == 'commands/checkAvailable':

            if Lights.busy == False:
                print("False")
                RESPONSE_MSG = json.dumps({ "status" : True })
                RESPONSE_TOPIC = 'results/checkAvailable'
                self.client.publish(RESPONSE_TOPIC, payload=RESPONSE_MSG, qos=0, retain=False)
            else:
                print("True")
                RESPONSE_MSG = json.dumps({ "status" : False })
                RESPONSE_TOPIC = 'results/checkAvailable'
                self.client.publish(RESPONSE_TOPIC, payload=RESPONSE_MSG, qos=0, retain=False)

        elif topic == 'results/checkCredentials':

                status = message['status']

                if status == 'True':
                    RESPONSE_MSG = json.dumps({ "color" : 'green' })
                    RESPONSE_TOPIC = 'action/state'
                    MQTT.scheduler.send('goto_green','stm_lights')
                elif status == 'False':
                    RESPONSE_MSG = json.dumps({ "color" : 'red' })
                    RESPONSE_TOPIC = 'action/state'
                    MQTT.scheduler.send('goto_red','stm_lights')

def mqtt_listen():
    global scheduler
    mqtt_listener = MQTT(scheduler)

def activate_lights():
    global scheduler

    lights = Lights()
    t0 = {'source': 'initial', 'target': 's_none', 'effect': 'on_init'}

    t1= {'trigger': 'goto_green', 'source': 's_none', 'target': 's_green', 'effect': 'on_green'}
    t2= {'trigger': 'goto_none', 'source': 's_green', 'target': 's_none', 'effect': 'on_none'}

    t3= {'trigger': 'goto_red', 'source': 's_none', 'target': 's_red', 'effect': 'on_red'}
    t4= {'trigger': 'goto_none', 'source': 's_red', 'target': 's_none', 'effect': 'on_none'}

    stm_lights= Machine(name='stm_lights', transitions=[t0, t1, t2, t3, t4], obj=lights)

    lights.stm = stm_lights
    scheduler.add_machine(stm_lights)
    scheduler.start()

    # scheduler.wait_until_finished()


mqtt_listen()
activate_lights()
