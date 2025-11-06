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

def run():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(host=BROKER_HOST, port=BROKER_PORT, keepalive=60)
    except Exception as e:
        print(f"Subscriber: Error connecting to broker at {BROKER_HOST}: {e}")
        return

    client.loop_forever()

if __name__ == '__main__':
    run()
