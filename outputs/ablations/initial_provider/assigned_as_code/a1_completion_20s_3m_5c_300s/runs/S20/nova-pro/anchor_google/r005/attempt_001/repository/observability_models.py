from typing import List, Dict

class LogModel:
    def __init__(self, message: str, correlation_id: str, severity: str):
        self.message = message
        self.correlation_id = correlation_id
        self.severity = severity

    @staticmethod
    def normalize(log_event: Dict) -> Dict:
        return {
            'name': log_event['message'],
            'customDimensions': {
                'correlation_id': log_event['correlation_id'],
                'severity': log_event['severity']
            }
        }

class LogQueryModel:
    def __init__(self, severity: str, start_time: str, end_time: str):
        self.severity = severity
        self.start_time = start_time
        self.end_time = end_time

class LogFetchModel:
    def __init__(self, field: str, value: str, start_time: str, end_time: str):
        self.field = field
        self.value = value
        self.start_time = start_time
        self.end_time = end_time