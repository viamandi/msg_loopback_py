import paho.mqtt.client as mqtt
import time
import random
import threading
from constants import BROKER_ADDRESS, BROKER_PORT, TOPIC

def publisher_thread_func(stop_event):
    """
    Function to be run in a separate thread for publishing messages.
    It stops when the stop_event is set.
    """
    
    def on_connect_pub(client, userdata, flags, rc):
        """Callback for when the publisher connects."""
        if rc == 0:
            print("Publisher: Connected to MQTT Broker!")
        else:
            print(f"Publisher: Failed to connect, return code {rc}\n")

    # Create and connect the publisher client
    pub_client = mqtt.Client(client_id="main-publisher-1")
    pub_client.on_connect = on_connect_pub
    pub_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    pub_client.loop_start()

    print("Publisher thread started. Publishing messages every 5 seconds...")
    while not stop_event.is_set():
        # Simulate a temperature reading
        temperature = round(random.uniform(20.0, 25.0), 2)
        message = f"{temperature}°C"
        
        # Publish the message
        result = pub_client.publish(TOPIC, message)
        status = result[0]
        if status == 0:
            print(f"-> Published `{message}` to topic `{TOPIC}`")
        else:
            print(f"-> Failed to send message to topic {TOPIC}")
        
        # Wait for 5 seconds or until the stop event is set
        stop_event.wait(5)
    
    print("Publisher thread stopping.")
    pub_client.loop_stop()
    pub_client.disconnect()

def run_subscriber():
    """
    Runs the subscriber client in the main thread.
    """
    def on_connect_sub(client, userdata, flags, rc):
        """Callback for when the subscriber connects."""
        if rc == 0:
            print("Subscriber: Connected to MQTT Broker!")
            client.subscribe(TOPIC)
        else:
            print(f"Subscriber: Failed to connect, return code {rc}\n")

    def on_message(client, userdata, msg):
        """Callback for when a message is received."""
        print(f"<- Received message: `{msg.payload.decode()}` on topic `{msg.topic}`")

    # Create and connect the subscriber client
    sub_client = mqtt.Client(client_id="main-subscriber-1")
    sub_client.on_connect = on_connect_sub
    sub_client.on_message = on_message
    sub_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    
    # This is a blocking call that processes network traffic
    sub_client.loop_forever()

if __name__ == '__main__':
    stop_event = threading.Event()
    
    # Create and start the publisher thread
    pub_thread = threading.Thread(target=publisher_thread_func, args=(stop_event,))
    pub_thread.start()

    print("Starting subscriber. Press Ctrl+C to exit.")
    try:
        run_subscriber()
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_event.set()  # Signal the publisher thread to stop
        pub_thread.join() # Wait for the publisher thread to finish
        print("Shutdown complete.")