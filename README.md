# ttm4115-base

SETUP:

1. Install mosquitto broker: https://mosquitto.org/download/
	-> mosquitto is automaticall started on 127.0.0.1:1883
	-> mosquitto does not automatically support websockets. To configure this, create a file mosquitto.conf in /etc/mosquitto/conf.d and type the following:

		listener 1883
		protocol mqtt
	
		listener 1884
		protocol websockets
	
	and run 'mosquitto -c /etc/mosquitto/conf.d/mosquitto.conf' to run mosquitto in the forground and activate the websockets. You might have to stop an already running broker with 'systemctl stop mosquitto'

2. Install MQTT.fx: http://www.jensd.de/apps/mqttfx/1.7.0/
	-> May need extra downloads after installing.
	-> Open MQTT.fx and press connect, you should be connected to the local mosquitto server.

3. Install pip with 'sudo apt install python3-pip' 

4. Install paho-mqtt for python with 'pip3 install paho-mqtt'
	-> This is for the python based broker

5. install stmpy with 'pip3 install stmpy'

6. Install Node-Red
  6.1 'sudo apt-get install build-essential'
  6.2 'bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)'
	-> We're not using apt because it does not contain vital checks or npm (to install mqtt)
  6.3 Install sqlite in node red: npm install node-red-node-sqlite

7. Install sense-hat if not already installed: pip3 install sense-hat


TO RUN:

1. start node red in one window - $ node-red-start
    -> Navigate to 127.0.0.1:1880 and press the Create and Insert nodes.
    -> The insert node inserts a single name "John Snow" into the database.
2. python stmpy.py
3. python sensehat.py
4. open the client.html file in a browser window. 
