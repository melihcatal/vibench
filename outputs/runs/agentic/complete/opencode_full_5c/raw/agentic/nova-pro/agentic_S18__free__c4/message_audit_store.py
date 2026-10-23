import json


def store_message_record(record):
    with open("message_audit.json", "a") as f:
        f.write(json.dumps(record) + "\n")
