import json


def normalize_log_event(log_event):
    return {
        "timestamp": log_event["timestamp"],
        "message": json.loads(log_event["message"]),
    }


def parse_log_response(response):
    return [normalize_log_event(event) for event in response["events"]]
