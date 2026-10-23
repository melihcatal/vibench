from datetime import datetime, timedelta
from google.cloud import logging as cloud_logging
from google.cloud.logging import DESCENDING
from observability_models import ErrorLogFilter

client = cloud_logging.Client()


def query_error_logs(filter_params: ErrorLogFilter) -> list[dict]:
    """Query recent error log entries filtered by severity and time range in Google Cloud Logging."""
    logger = client.logger('application-logs')
    
    filter_str = (
        f"severity >= {filter_params.min_severity} "
        f"AND timestamp >= \"{filter_params.start_time.isoformat()}\" "
        f"AND timestamp <= \"{filter_params.end_time.isoformat()}\""
    )
    
    entries = logger.list_entries(
        filter_=filter_str,
        order_by=DESCENDING,
        max_results=filter_params.max_results
    )
    
    return [entry.to_api_repr() for entry in entries]