from typing import List, Dict


class LogEvent:
    def __init__(self, timestamp: int, message: str):
        self.timestamp = timestamp
        self.message = message

    def to_dict(self) -> Dict:
        return {"timestamp": self.timestamp, "message": self.message}

    @classmethod
    def from_dict(cls, data: Dict) -> "LogEvent":
        return cls(data["timestamp"], data["message"])


class LogQueryResponse:
    def __init__(self, results: List[Dict]):
        self.results = results

    def to_dict(self) -> Dict:
        return {"results": [result.to_dict() for result in self.results]}
