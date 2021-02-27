import time
import sqlite3
from flask import g
from flask import Flask, request
from central.database_adapter import DatabaseAdapter
app = Flask(__name__)
database = DatabaseAdapter()

last_row_id = 0

@app.route('/')
def hello_world():
    return 'Hello, World!', 200


@app.route('/new/value', methods=['POST'])
def new_value():
    payload = request.json
    new_last_row_id = database.save_measurement(payload["name"], payload["value"], time.time())
    print(f"New data! {payload} {new_last_row_id}")
    return "OK"


def start():
    app.run(port=5050, host="0.0.0.0", debug=True)
