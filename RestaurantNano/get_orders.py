import paho.mqtt.client as mqtt
import sys
import json
from send_data_to_BigQuery import send_data_to_bigquery

broker = "10.13.190.44"
port = 1885
topic1 = "jetson/order"

def get_product_id(name):
    with open('product_to_dish.json','r') as f:
        product_mapping = json.load(f)
    for p_id, dish in product_mapping.items():
        if name == dish:
            return p_id

def on_connect(client, userdata, flags,rc):
    client.subscribe(topic1)
    
def on_message(client, userdata, msg):
    print("Message received: " + msg.payload.decode())
    convert_hashmap(msg.payload.decode())

def convert_hashmap(msg):
    hashmap = json.loads(msg)
    #print(hashmap)
    p_ids = []
    for key,value in hashmap.items():
       
        if key == "id":
            u_id = hashmap[key]
        else:
            val = get_product_id(key)
            p_ids.append(val)
    send_to_cloud(p_ids,u_id)
    print(p_ids)
    print(u_id)

def send_to_cloud(pids,uid):    
    for val in pids:
       data = {}
       data['UserId'] = uid
       data['ProductId'] = val
       send_data_to_bigquery(data)

     


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
