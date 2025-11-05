import paho.mqtt.client as mqtt
import os

# Citim adresa broker-ului din variabila de mediu MQTT_BROKER_HOST
# Dacă nu este setată, folosim 'localhost'
BROKER_ADDRESS = os.getenv('MQTT_BROKER_HOST', 'localhost')
TOPIC = "test/topic"

def on_connect(client, userdata, flags, rc):
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
        client.connect(BROKER_ADDRESS, 1884)
    except Exception as e:
        print(f"Subscriber: Error connecting to broker at {BROKER_ADDRESS}: {e}")
        return

    client.loop_forever()

if __name__ == '__main__':
    run()
