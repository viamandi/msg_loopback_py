import paho.mqtt.client as mqtt
import time
import os
from constants import BROKER_HOST, BROKER_PORT, TOPIC

# Semnătura corectă pentru CallbackAPIVersion.VERSION2
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Publisher: Connected to MQTT Broker!")
    else:
        print(f"Publisher: Failed to connect, return code {reason_code}\n")

def publish(client):
    msg_count = 0
    while True:

