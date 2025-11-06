# d:\personal\separate_py\msg_loopback_docker_py\main.py

import paho.mqtt.client as mqtt
import time
import threading
import os # Importăm modulul 'os'

# --- MQTT Broker settings ---
# Preluăm adresa brokerului din variabila de mediu 'MQTT_BROKER_HOST'.
# Dacă variabila nu este setată, folosim 'localhost' ca valoare implicită.
BROKER = os.getenv('MQTT_BROKER_HOST', 'localhost')
PORT = 1883
TOPIC_PUB = "test/topic/pub"
TOPIC_SUB = "test/topic/sub"
CLIENT_ID_PUB = "python-publisher"
CLIENT_ID_SUB = "python-subscriber"

# Flag pentru a opri buclele
stop_flag = threading.Event()

# --- Publisher ---
def on_connect_pub(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Publisher: Connected to MQTT Broker!")
    else:
        print(f"Publisher: Failed to connect, return code {rc}\n")

def publisher_loop():
    client_pub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID_PUB)
    client_pub.on_connect = on_connect_pub
    try:
        client_pub.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Publisher: Error connecting to broker at {BROKER}: {e}")
        return

    client_pub.loop_start()
    count = 0
    while not stop_flag.is_set():
        count += 1
        message = f"Hello from Publisher! Message #{count}"
        result = client_pub.publish(TOPIC_PUB, message)
        status = result.rc
        if status == 0:
            print(f"Publisher: Sent `{message}` to topic `{TOPIC_PUB}`")
        else:
            print(f"Publisher: Failed to send message to topic {TOPIC_PUB}")
        time.sleep(5)
    client_pub.loop_stop()
    client_pub.disconnect()
    print("Publisher: Disconnected and stopped.")

# --- Subscriber ---
def on_connect_sub(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Subscriber: Connected to MQTT Broker!")
        client.subscribe(TOPIC_PUB)
    else:
        print(f"Subscriber: Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    print(f"Subscriber: Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    # Loopback: Publish a response
    response_message = f"ACK: {msg.payload.decode()}"
    client.publish(TOPIC_SUB, response_message)
    print(f"Subscriber: Sent `{response_message}` to topic `{TOPIC_SUB}`")

def subscriber_loop():
    client_sub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID_SUB)
    client_sub.on_connect = on_connect_sub
    client_sub.on_message = on_message
    try:
        client_sub.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Subscriber: Error connecting to broker at {BROKER}: {e}")
        return

    client_sub.loop_forever()
    print("Subscriber: Disconnected and stopped.")

# --- Main execution ---
if __name__ == "__main__":
    print("Pornirea publisher-ului si subscriber-ului MQTT...")

    # Pornim publisher-ul într-un thread separat
    pub_thread = threading.Thread(target=publisher_loop)
    pub_thread.start()

    # Pornim subscriber-ul în thread-ul principal
    # Adăugăm un try-except pentru a prinde KeyboardInterrupt (Ctrl+C)
    try:
        subscriber_loop()
    except KeyboardInterrupt:
        print("\nOprire solicitată. Se închid conexiunile...")
        stop_flag.set()
        pub_thread.join() # Așteptăm ca thread-ul publisher-ului să se termine
        print("Aplicație oprită complet.")

