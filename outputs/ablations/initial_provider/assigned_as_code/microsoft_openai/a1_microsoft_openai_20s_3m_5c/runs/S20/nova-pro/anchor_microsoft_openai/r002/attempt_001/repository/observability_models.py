from datetime import datetime, timezone


def normalize_log_event(event):
    event['TimeGenerated'] = datetime.fromisoformat(event['TimeGenerated']).replace(tzinfo=timezone.utc)
    return event


def parse_log_response(response):
    if response.tables:
        return [normalize_log_event(row) for row in response.tables[0].rows]
    return []