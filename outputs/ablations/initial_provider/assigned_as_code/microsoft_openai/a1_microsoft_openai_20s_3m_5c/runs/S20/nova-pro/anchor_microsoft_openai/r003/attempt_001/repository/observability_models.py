from datetime import datetime, timezone


def create_log_event(payload):
    event = dict(payload['event'])
    event['TimeGenerated'] = datetime.fromtimestamp(payload.get('timestamp_ms', time.time() * 1000) / 1000, tz=timezone.utc).isoformat()
    return event


def parse_log_response(response):
    return response.tables[0].rows if response.tables else []