import json

def store_message(message):
    with open('message_audit.json', 'a') as f:
        f.write(json.dumps(message.__dict__) + '\n')