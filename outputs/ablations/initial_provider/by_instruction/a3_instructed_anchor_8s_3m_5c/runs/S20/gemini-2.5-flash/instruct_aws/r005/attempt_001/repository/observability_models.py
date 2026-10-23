import json
from typing import Dict, Any, List, Optional

class LogEvent:
    def __init__(self, message: Dict[str, Any], timestamp: int, log_stream_name: str):
        self.message = message
        self.timestamp = timestamp
        self.log_stream_name = log_stream_name

    def to_aws_cloudwatch_format(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'message': json.dumps(self.message)
        }

class LogQueryResult:
    def __init__(self, fields: List[Dict[str, str]], records: List[List[Dict[str, str]]]):
        self.fields = fields
        self.records = records

    @classmethod
    def from_aws_cloudwatch_insights_response(cls, response: Dict[str, Any]):
        fields = response.get('results', [])[0] if response.get('results') else []
        records = response.get('results', [])
        return cls(fields, records)
