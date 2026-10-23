import json

def normalize_log_event(log_event):
    return json.dumps(log_event)

def parse_log_response(response):
    return response['results']