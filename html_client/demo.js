

// Create a client instance
client = new Paho.MQTT.Client('localhost', 1884, "1234");
console.log(location.hostname)
console.log(location.port)

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("results/checkAvailable");
  client.subscribe("action/state");
  message = new Paho.MQTT.Message("Hello");
  message.destinationName = "connect";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives. Handles action.
function onMessageArrived(message) {

  var node = document.createElement("LI");
  console.log("onMessageArrived:"+message.payloadString);
  result = JSON.parse(message.payloadString);
  topic = message.destinationName;
  console.log(topic);
  
  //If the STMPY machine is idle, ask database if name is valid
  // If not, stop
  if (topic == 'results/checkAvailable'){
    if (result["status"] == true){
      log("Success");
      checkName(window.name)
    } else {
      log("Not idle");
    }
  } else if (topic == 'action/state'){
      if (result["color"] == 'green'){
          enableWalkthrough();
          log("Success");
        }
      if (result["color"] == 'none'){
          disableWalkthrough();
        }
      if (result["color"] == 'red'){
          log(name + " is not in the database...")
        }
    }
}

// Called when operator is pressing the button, initiates name check
function enterName() {
  window.name = document.getElementById("name").value;
  log("Checking if STMPY is idle...");
  message = new Paho.MQTT.Message(JSON.stringify({"status":"none"}));
  message.destinationName = "commands/checkAvailable";
  client.send(message);
}

function checkName(name){
  var json_obj = {name: name};
  message = new Paho.MQTT.Message(JSON.stringify(json_obj))
  message.destinationName = "commands/checkCredentials";
  client.send(message)
  log("Checking credentials");
}

function submitWalkthrough(){
  var json_obj = {name: name};
  message = new Paho.MQTT.Message(JSON.stringify(json_obj))
  message.destinationName = "update/walkthrough";
  client.send(message)
  log("Updating boarding status for: " + name);
}

function log(logmsg){
  var node = document.createElement("LI");
  var textnode = document.createTextNode(logmsg);
  node.appendChild(textnode);
  document.getElementById("alerts").appendChild(node);
}

function resetLog(){
  var ul = document.getElementById("alerts");
  while(ul.firstChild) ul.removeChild(ul.firstChild);
}

function disableWalkthrough(){
    var btn = document.getElementById("walkthrough-button")
    btn.disabled = true;
}
function enableWalkthrough(){
    var btn = document.getElementById("walkthrough-button")
    btn.disabled = false;
}

