from dataclasses import dataclass
from datetime import datetime, timezone


def to_iso8601(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return value


@dataclass
class LogTimeRange:
    start_time: datetime
    end_time: datetime

    def to_payload(self):
        return {'start_time': to_iso8601(self.start_time), 'end_time': to_iso8601(self.end_time)}


def normalize_log_event(payload, severity=None, correlation_id=None, locale=None):
    event = dict(payload)
    if severity is not None:
        event['severity'] = severity
    if correlation_id is not None:
        event['correlation_id'] = correlation_id
    if locale is not None:
        event['locale'] = locale
    return event


def extract_table_rows(query_response):
    if hasattr(query_response, 'tables') and query_response.tables:
        table = query_response.tables[0]
        columns = [column.name for column in table.columns]
        return [dict(zip(columns, row)) for row in table.rows]
    return []
