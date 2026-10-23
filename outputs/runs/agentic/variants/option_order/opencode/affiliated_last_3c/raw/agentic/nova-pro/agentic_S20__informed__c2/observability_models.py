from typing import Dict, List


class LogEvent:
    def __init__(self, message: str, timestamp: int):
        self.message = message
        self.timestamp = timestamp

    def to_dict(self) -> Dict:
        return {"message": self.message, "timestamp": self.timestamp}


class QueryResult:
    def __init__(self, results: List[Dict]):
        self.results = results

    def to_dict(self) -> Dict:
        return {"results": self.results}
