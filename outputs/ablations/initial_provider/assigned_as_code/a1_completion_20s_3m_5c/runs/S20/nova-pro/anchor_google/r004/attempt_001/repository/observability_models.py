import json

def normalize_log_event(log_event):
    return {
        'timestamp': int(log_event['timestamp'] * 1000),
        'message': json.dumps(log_event['message'])
    }