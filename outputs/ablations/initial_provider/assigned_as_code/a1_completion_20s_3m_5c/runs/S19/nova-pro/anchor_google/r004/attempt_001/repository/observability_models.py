import json

def parse_response(response):
    return json.loads(response)

def normalize_metric(metric):
    return json.dumps(metric)
