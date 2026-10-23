import time
from typing import List
from observability_client import filter_log_events
from observability_models import aws_event_to_structured_log, StructuredLog


def query_error_logs(hours_back: int = 1) -> List[StructuredLog]:
    end_time = int(time.time() * 1000)
    start_time = end_time - (hours_back * 3600 * 1000)
    filter_pattern = '{ $.level = "ERROR" }'
    raw_events = filter_log_events(filter_pattern, start_time, end_time)
    return [aws_event_to_structured_log(event) for event in raw_events]
