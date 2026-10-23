import time
from observability_client import CloudWatchLogsClient
from observability_models import parse_log_entry

def query_error_logs(log_group_name, start_time_ms, end_time_ms, severity="ERROR", region_name=None, limit=None):
    client = CloudWatchLogsClient(region_name=region_name)
    
    # CloudWatch Logs filter pattern for severity. Adjust based on actual log format.
    # Assuming 'severity' is a field in the JSON log message.
    filter_pattern = f'{{ $.severity = "{severity}" }}'

    log_events = client.filter_log_events(
        log_group_name,
        start_time_ms,
        end_time_ms,
        filter_pattern=filter_pattern,
        limit=limit
    )

    parsed_logs = [parse_log_entry(event) for event in log_events]
    return {"logs": parsed_logs}
