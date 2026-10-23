import json


def persist_message_record(message):
    with open('message_audit.json', 'a') as f:
        f.write(json.dumps(message) + '\n')