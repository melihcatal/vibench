import json

class LogEntry:
    def __init__(self, log_name, resource_type, labels, payload, timestamp=None):
        self.log_name = log_name
        self.resource_type = resource_type
        self.labels = labels
        self.payload = payload
        self.timestamp = timestamp

    def to_json(self):
        return json.dumps({
            "log_name": self.log_name,
            "resource_type": self.resource_type,
            "labels": self.labels,
            "payload": self.payload,
            "timestamp": str(self.timestamp) if self.timestamp else None
        })

class QueryFilter:
    def __init__(self, severity=None, time_range_start=None, time_range_end=None, text_search=None, fields=None):
        self.severity = severity
        self.time_range_start = time_range_start
        self.time_range_end = time_range_end
        self.text_search = text_search
        self.fields = fields or {}

    def to_filter_string(self):
        filters = []
        if self.severity:
            filters.append(f"severity>=\"{self.severity.upper()}\"")
        if self.time_range_start:
            filters.append(f"timestamp>=\"{self.time_range_start.isoformat()}Z\"")
        if self.time_range_end:
            filters.append(f"timestamp<=\"{self.time_range_end.isoformat()}Z\"")
        if self.text_search:
            filters.append(f"textPayload:\"{self.text_search}\" OR jsonPayload:\"{self.text_search}\"")
        for field, value in self.fields.items():
            filters.append(f"jsonPayload.{field}=\"{value}\"")
        return " AND ".join(filters)
