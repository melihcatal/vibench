from typing import Dict, Any, List

class LogEvent:
    def __init__(self, timestamp: int, message: Dict[str, Any]):
        self.timestamp = timestamp
        self.message = message

class StructuredLogRequest:
    def __init__(self, log_group_name: str, log_stream_name: str, message: Dict[str, Any]):
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.message = message

class CorrelatedLogsRequest:
    def __init__(self, log_group_name: str, log_stream_name: str, correlation_id: str, messages: List[Dict[str, Any]]):
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.correlation_id = correlation_id
        self.messages = messages

class QueryLogsRequest:
    def __init__(self, log_group_names: List[str], start_time: int, end_time: int, search_term: str = None, filter_field: str = None, filter_value: str = None):
        self.log_group_names = log_group_names
        self.start_time = start_time
        self.end_time = end_time
        self.search_term = search_term
        self.filter_field = filter_field
        self.filter_value = filter_value

class LogQueryResponse:
    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results
