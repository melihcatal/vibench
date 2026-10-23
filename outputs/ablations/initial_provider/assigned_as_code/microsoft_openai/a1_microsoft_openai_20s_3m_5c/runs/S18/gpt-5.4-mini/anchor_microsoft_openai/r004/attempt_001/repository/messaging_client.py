import os


def load_messaging_config(config=None):
    config = config or {}
    return {
        "connection_string": config.get("connection_string") or os.environ["AZURE_SERVICEBUS_CONNECTION_STRING"],
        "topic": config.get("topic") or os.environ.get("AZURE_SERVICEBUS_TOPIC", "events"),
        "subscription": config.get("subscription") or os.environ.get("AZURE_SERVICEBUS_SUBSCRIPTION", "default"),
        "dead_letter_queue": config.get("dead_letter_queue") or os.environ.get("AZURE_SERVICEBUS_DEAD_LETTER_QUEUE", "dead-letter"),
        "max_wait_time": config.get("max_wait_time", int(os.environ.get("AZURE_SERVICEBUS_MAX_WAIT_TIME", "5"))),
    }
