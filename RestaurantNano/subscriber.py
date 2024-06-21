import paho.mqtt.client as mqtt
import sys
from predict_model import main_func
# MQTT settings
broker = "10.13.190.44"
port = 1885
topic1 = "jetson/unique_id"
topic2 = "jetson/prediction"

def on_connect(client, userdata, flags,rc):
    client.subscribe(topic1)
    
def on_message(client, userdata, msg):
    print("Message received: " + msg.payload.decode())
    out = main_func(msg.payload.decode())
    #print(out)
    publish(client,main_func(msg.payload.decode()))

def publish(client,out):
    client.publish(topic2,out)

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
if client.connect(broker,port,60) != 0:
    print("could not connect to MQTT broker")
    sys.exit(-1)


# Blocking loop to process network traffic and dispatch callbacks
#try:
  #  print("Press CNTRL+C to exit")
client.loop_forever()
#except:
   # print("Disconnecting from broker")


client.disconnect()
