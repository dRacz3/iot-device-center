import os


class AppConfig:
    # Communication related
    MQTT_BROKER_ADDRESS = os.getenv("MQTT_BROKER_ADDRESS", "localhost")
    MQTT_TOPIC_PREFIX = "home"

    # Database related
    DATABASE_NAME = "database.db"
    TABLE_NAME = "MEASUREMENTS"
