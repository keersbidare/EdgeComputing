import random
import paho.mqtt.client as mqtt
import time
import uuid
import sys
import json

def display_dishes(food_menu):
    print("-------------------------Food Menu:------------------------------------------------")
    print("----Food ID------------------Item-------------------------Cost---------------------")
    print("-----------------------------------------------------------------------------------")
    for idx,(item,cost) in enumerate(food_menu.items(),start=1):
        print(f"    {idx:<25}{item:<29}${cost}")

dishes = [
	    'Pizza', 'Burger', 'Pasta', 'Sushi', 'Salad', 'Taco', 'Steak', 'Sandwich', 
	    'Soup', 'Curry', 'Fried Chicken', 'Lasagna', 'Paella', 'Falafel', 'Ramen', 
	    'Burrito', 'Kebab', 'Dim Sum', 'Peking Duck', 'Moussaka', 'Goulash', 'Chow Mein', 
	    'Biryani', 'Pho', 'Miso Soup', 'Gumbo', 'Jambalaya', 'Fish and Chips', 'Empanadas', 
	    'Croissant', 'Quiche', 'Tiramisu', 'Cheesecake', 'Pancakes', 'Waffles'
	]
order = {}
def find_cost(dishes):
    food_costs = {}
    for food in dishes:
        cost = random.randint(10,20)
        food_costs[food] = cost
    return food_costs

food_menu = find_cost(dishes)
display_dishes(food_menu)
print("\n")
print("Enter the dish id and the quantity in the respective fields as shown below,type 0 when you are done ordering:\n")
print("Enter the dish ID (or 0 to stop) : 4")
print("Enter the quantity : 3")
print("\n")
while True:
    dish_id = int(input("Enter the dish ID (or 0 to stop):"))
    if dish_id == 0:
        break
    quantity = int(input("Enter the quantity :"))
    order[dishes[dish_id-1]] = quantity
    print("\n")


unique_id = 'A370Z6I5GBWU44'
order['id'] = unique_id
broker = "192.168.206.59"
port = 1885
topic = "jetson/order"
client = mqtt.Client()
if client.connect(broker,port,60)!=0:
    sys.exit()
order_json = json.dumps(order)
client.publish(topic, order_json)

