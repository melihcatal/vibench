import os
import time
import json
from typing import Dict, Any, List, Optional
from observability_models import CloudWatchConfig, StructuredLogData, LogEvent, QueryResultRaw, QueryResult

def get_cloudwatch_config() -> CloudWatchConfig:
    return {
        'log_group': os.getenv('CLOUDWATCH_LOG_GROUP', 'default-log-group'),
        'log_stream': os.getenv('CLOUDWATCH_LOG_STREAM', 'default-stream'),
        'region': os.getenv('AWS_REGION', 'us-east-1')
    }

def create_log_event(data: StructuredLogData) -> LogEvent:
    timestamp = int(time.time() * 1000)
    message_data = data.copy()
    message = json.dumps(message_data)
    return {
        'timestamp': timestamp,
        'message': message
    }

def create_correlated_log_events(events: List[StructuredLogData], correlation_id: str) -> List[LogEvent]:
    for event in events:
        event['correlation_id'] = correlation_id
    return [create_log_event(event) for event in events]

def build_error_query(severity: str = 'ERROR', limit: int = 20) -> str:
    filter_expr = f'@message like /"level":"{severity}"/'
    return f'fields @timestamp, @message | filter {filter_expr} | sort @timestamp desc | limit {limit}'

def build_field_filter_query(field: str, value: str, limit: int = 20) -> str:
    filter_expr = f'@message like /"{field}":"{value}"/'
    return f'fields @timestamp, @message | filter {filter_expr} | sort @timestamp desc | limit {limit}'

def normalize_query_results(raw_results: QueryResultRaw) -> QueryResult:
    normalized = []
    for row in raw_results:
        result = {}
        for field in row:
            result[field['field']] = field['value']
        normalized.append(result)
    return normalized
