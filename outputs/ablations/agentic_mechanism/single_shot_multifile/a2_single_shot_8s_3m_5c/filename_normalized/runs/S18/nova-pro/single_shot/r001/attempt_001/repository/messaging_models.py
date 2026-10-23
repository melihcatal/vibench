import json

def normalize_message_data(data):
    return json.dumps(data).encode('utf-8')

def parse_message_data(message):
    return json.loads(message.data)