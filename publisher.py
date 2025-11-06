import paho.mqtt.client as mqtt
import time
import os

# Citim adresa broker-ului din variabila de mediu MQTT_BROKER_HOST
# Dacă nu este setată, folosim 'localhost'BROKER_ADDRESS = "127.0.0.7"
BROKER_HOST = "hivemq"
BROKER_PORT = 1883
TOPIC = "test/topic"

def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
        print("Publisher: Connected to MQTT Broker!")
    else:
        print(f"Publisher: Failed to connect, return code {rc}\n")

def publish(client):
    msg_count = 0
    while True:
        time.sleep(5)
        msg = f"message: {msg_count}"
        result = client.publish(TOPIC, msg)
        status = result[0]
        if status == 0:
            print(f"Publisher: Sent `{msg}` to topic `{TOPIC}`")
        else:
            print(f"Publisher: Failed to send message to topic {TOPIC}")
        msg_count += 1

def run():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Publisher")
    client.on_connect = on_connect
    try:
        client.connect(host=BROKER_HOST, port=BROKER_PORT, keepalive=60)
    except Exception as e:
        print(f"Publisher: Error connecting to broker at {BROKER_HOST}: {e}")
        return

    client.loop_start()
    publish(client)
    client.loop_stop()

if __name__ == '__main__':
    run()
