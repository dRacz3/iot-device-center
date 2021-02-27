import time
from flask import Flask, request
from adapters.database_adapter import DatabaseAdapter
from adapters.mqtt_adapter import MQTTAdapter, MQTTConfig
from central.config import AppConfig as config
app = Flask(__name__)


database = DatabaseAdapter(config.DATABASE_NAME, config.TABLE_NAME)
mqtt = MQTTAdapter(MQTTConfig(host=config.MQTT_BROKER_ADDRESS))

@app.route('/')
def hello_world():
    return 'Hello, World!', 200


@app.route('/new/value', methods=['POST'])
def new_value():
    payload = request.json
    new_last_row_id = database.save_measurement(payload["name"], payload["value"], time.time())
    print(f"New data! {payload} {new_last_row_id}")
    mqtt.publish(f"{config.MQTT_TOPIC_PREFIX}/{payload['name']}", payload=payload["value"])
    return "OK"


def start():
    mqtt.connect()
    app.run(port=5050, host="0.0.0.0", debug=True)
