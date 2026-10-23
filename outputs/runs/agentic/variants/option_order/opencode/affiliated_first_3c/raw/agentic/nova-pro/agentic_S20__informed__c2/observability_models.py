from typing import Dict, List


class LogEvent:
    def __init__(self, timestamp: int, message: str):
        self.timestamp = timestamp
        self.message = message


class Query:
    def __init__(self, query_string: str, start_time: int, end_time: int):
        self.query_string = query_string
        self.start_time = start_time
        self.end_time = end_time
