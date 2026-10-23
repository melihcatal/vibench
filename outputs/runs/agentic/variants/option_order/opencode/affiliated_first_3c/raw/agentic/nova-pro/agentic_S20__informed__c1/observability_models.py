from typing import Dict, List


class LogEvent:
    def __init__(self, timestamp: int, message: str):
        self.timestamp = timestamp
        self.message = message


class FilterPattern:
    def __init__(self, pattern: str):
        self.pattern = pattern
