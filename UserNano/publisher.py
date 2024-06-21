import paho.mqtt.client as mqtt
import time
import uuid
import sys

# Generate a unique ID for the Jetson Nano
unique_id = 'A370Z6I5GBWU44'
print("Begining of the program")
# MQTT settings
broker = "192.168.206.59"
port = 1885
topic = "jetson/unique_id"
flag = 0
topic1 = "jetson/prediction"

sub_ack = False
def subscriber(client):
    global sub_ack
    sub_ack = False
    client.subscribe(topic1)
def on_message(client,userdata,msg):
    flag = 0
    print(msg.payload.decode())
def on_subscribe(client,userdata,mid,granted_qos):
    global sub_ack
    print("Subscribed")
    sub_ack = True

def publish():
    print("Publisher started")
    client = mqtt.Client()
    client.on_message = on_message
    client.on_subscriber = on_subscribe
    if client.connect(broker, port,60)!= 0:
        sys.exit(-1)
    client.publish(topic,unique_id,0)
    while not sub_ack:
        subscriber(client)
        time.sleep(1)

    #try:
    # print("CNTRL+C to stop")
    client.loop_forever()
    #except:
        # print("Disconnecting")


