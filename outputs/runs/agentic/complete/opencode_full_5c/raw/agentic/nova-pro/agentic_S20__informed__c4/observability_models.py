from typing import Dict, List


class LogEntry:
    def __init__(self, message: str, timestamp: int):
        self.message = message
        self.timestamp = timestamp

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data["message"], data["timestamp"])


class LogQueryResponse:
    def __init__(self, events: List[LogEntry]):
        self.events = events

    @classmethod
    def from_dict(cls, data: Dict):
        events = [LogEntry.from_dict(event) for event in data["events"]]
        return cls(events)
