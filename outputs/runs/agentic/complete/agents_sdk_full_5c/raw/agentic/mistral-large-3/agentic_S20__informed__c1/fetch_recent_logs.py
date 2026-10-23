from datetime import datetime, timedelta
from google.cloud import logging as cloud_logging
from google.cloud.logging import DESCENDING
from observability_models import RecentLogFilter

client = cloud_logging.Client()


def fetch_recent_logs(filter_params: RecentLogFilter) -> list[dict]:
    """Retrieve recent log results filtered by field values and time range in Google Cloud Logging."""
    logger = client.logger(filter_params.log_name)
    
    filter_parts = [
        f"timestamp >= \"{filter_params.start_time.isoformat()}\" ",
        f"timestamp <= \"{filter_params.end_time.isoformat()}\" "
    ]
    
    if filter_params.field_filters:
        for field, value in filter_params.field_filters.items():
            filter_parts.append(f"jsonPayload.{field} = \"{value}\" ")
    
    filter_str = "AND ".join(filter_parts)
    
    entries = logger.list_entries(
        filter_=filter_str,
        order_by=DESCENDING,
        max_results=filter_params.max_results
    )
    
    return [entry.to_api_repr() for entry in entries]