from typing import Any, Dict, List, Union


class LogQueryRequest:
    def __init__(self, query: str, start_time: str, end_time: str, fields: List[str]):
        self.query = query
        self.start_time = start_time
        self.end_time = end_time
        self.fields = fields


class LogQueryResponse:
    def __init__(self, status: str, results: List[Dict[str, Any]]):
        self.status = status
        self.results = results


def normalize_log_fields(log_entry: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    normalized_entry = {}
    for field in fields:
        if field in log_entry:
            normalized_entry[field] = log_entry[field]
    return normalized_entry


def format_log_response(response: LogQueryResponse) -> List[Dict[str, Any]]:
    formatted_response = []
    for entry in response.results:
        formatted_response.append(normalize_log_fields(entry, ['timestamp', 'level', 'message']))
    return formatted_response