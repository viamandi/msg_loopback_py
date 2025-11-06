import paho.mqtt.client as mqtt
import os

# Citim adresa broker-ului din variabila de mediu MQTT_BROKER_HOST
# Dacă nu este setată, folosim 'localhost'
BROKER_HOST = "hostmq"
BROKER_PORT = 1883
TOPIC = "test/topic"

def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber: Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f"Subscriber: Failed to connect, return code {rc}\n")

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
