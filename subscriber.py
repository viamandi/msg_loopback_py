import paho.mqtt.client as mqtt
import os
from constants import BROKER_HOST, BROKER_PORT, TOPIC

# Semnătura corectă pentru CallbackAPIVersion.VERSION2
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Subscriber: Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f"Subscriber: Failed to connect, return code {reason_code}\n")

def on_message(client, userdata, msg):
    print(f"Subscriber: Received `{msg.payload.decode()}` from `{msg.topic}` topic")

