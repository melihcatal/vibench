from datetime import datetime, timezone


def normalize_log_event(payload):
    timestamp_ms = payload.get('timestamp_ms', time.time() * 1000)
    event = dict(payload['event'])
    event['TimeGenerated'] = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()
    return event


def parse_log_response(response):
    if response.tables:
        return response.tables[0].rows
    return []
