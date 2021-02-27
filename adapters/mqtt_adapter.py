import paho.mqtt.client as mqtt
from dataclasses import dataclass
import json

@dataclass
class MQTTConfig:
    host : str
    port : int = 1883
    timeout : int = 60

class MQTTAdapter:
    def __init__(self, config : MQTTConfig):
        self.config = config
        self.client = mqtt.Client()

        self.bootstrap_client()

    def bootstrap_client(self):
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

    def connect(self):
        self.client.connect(self.config.host, self.config.port, self.config.timeout)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")
        client.subscribe("home/#")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def on_publish(self, client, *args):
        pass

    def on_subscribe(self, *args,**kwargs):
        print(f"Subscribed : {args},{kwargs}")

    def loop_forever(self):
        self.client.loop_forever()

    def publish(self, topic : str, payload : dict):
        if not self.client.is_connected():
            self.connect()
        r = self.client.publish(topic=topic, payload=json.dumps(payload))
        print(f"Published to topic '{topic}'-> {payload}")


if __name__=="__main__":
    import os
    broker_address = os.getenv("MQTT_BROKER_ADDRESS", "192.168.0.206")
    config = MQTTConfig(broker_address)
    mqtt_adapter = MQTTAdapter(config)
    mqtt_adapter.connect()
    import time
    i = 0
    while True:
        i += 1
        mqtt_adapter.publish("home/test", i)
        time.sleep(2)
