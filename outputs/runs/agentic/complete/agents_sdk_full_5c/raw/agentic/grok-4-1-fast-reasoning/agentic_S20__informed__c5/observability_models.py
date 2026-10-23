def build_error_query(severity: str, start_time: int, end_time: int, limit: int = 100) -> str:
    return f'''fields @timestamp, @message
| filter @message like /"level":"{severity}"/
| filter @timestamp >= {start_time} and @timestamp <= {end_time}
| sort @timestamp desc
| limit {limit}'''

def build_recent_logs_query(filter_pattern: str, start_time: int, end_time: int, limit: int = 100) -> str:
    return f'''fields @timestamp, @message
| filter @message like /{filter_pattern}/
| filter @timestamp >= {start_time} and @timestamp <= {end_time}
| sort @timestamp desc
| limit {limit}'''
