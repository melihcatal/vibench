from dataclasses import dataclass
from datetime import datetime, timezone


def _to_iso8601(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return value


def normalize_log_event(event):
    item = dict(event)
    if 'timestamp' in item:
        item['timestamp'] = _to_iso8601(item['timestamp'])
    if 'TimeGenerated' in item:
        item['TimeGenerated'] = _to_iso8601(item['TimeGenerated'])
    if 'severity' in item and item['severity'] is not None:
        item['severity'] = str(item['severity']).upper()
    if 'message' in item and item['message'] is not None:
        item['message'] = str(item['message'])
    return item


@dataclass
class LogQuery:
    start_time: str
    end_time: str
    filters: dict


@dataclass
class LogResponse:
    items: list
    count: int
