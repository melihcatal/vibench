from typing import Dict, List

class LogEvent:
    def __init__(self, timestamp: int, message: str):
        self.timestamp = timestamp
        self.message = message

class LogQuery:
    def __init__(self, start_time: int, end_time: int, filter_pattern: str):
        self.start_time = start_time
        self.end_time = end_time
        self.filter_pattern = filter_pattern

def normalize_log_event(log_event: Dict) -> LogEvent:
    return LogEvent(log_event['timestamp'], log_event['message'])

def normalize_log_events(log_events: List[Dict]) -> List[LogEvent]:
    return [normalize_log_event(log_event) for log_event in log_events]