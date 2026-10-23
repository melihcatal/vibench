from typing import Any, Dict, List


class LogQueryRequest:
    def __init__(self, query: str, start_time: str, end_time: str):
        self.query = query
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'query': self.query,
            'startTime': self.start_time,
            'endTime': self.end_time
        }


class LogQueryResponse:
    def __init__(self, logs: List[Dict[str, Any]]):
        self.logs = logs

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LogQueryResponse':
        return LogQueryResponse(logs=data.get('logs', []))


def normalize_log(log: Dict[str, Any]) -> Dict[str, Any]:
    normalized_log = {
        'timestamp': log.get('timestamp'),
        'message': log.get('message'),
        'severity': log.get('severity', 'INFO')
    }
    return normalized_log
