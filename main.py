import threading
import signal
import sys
import publisher
import subscriber

# Funcție pentru a opri programul elegant
def signal_handler(sig, frame):
    print('\nOprire program...')
    sys.exit(0)

if __name__ == "__main__":
    print("Pornirea publisher-ului si subscriber-ului MQTT...")
    # Înregistrează handler-ul pentru Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Creează și pornește thread-ul pentru publisher
    publisher_thread = threading.Thread(target=publisher.run)
    publisher_thread.daemon = True  # Permite programului principal să se închidă chiar dacă thread-ul rulează
    publisher_thread.start()

    # Creează și pornește thread-ul pentru subscriber
    subscriber_thread = threading.Thread(target=subscriber.run)
    subscriber_thread.daemon = True
    subscriber_thread.start()

    # Așteaptă ca thread-urile să ruleze (programul se va opri cu Ctrl+C)
    while True:
        pass
