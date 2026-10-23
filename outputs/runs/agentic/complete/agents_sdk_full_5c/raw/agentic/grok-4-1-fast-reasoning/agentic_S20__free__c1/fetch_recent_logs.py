from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import get_datadog_configuration
from observability_models import build_query_body, parse_log_response
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_query_api import LogsQueryApi

def fetch_recent_logs(field_filter: str, value: str, hours_back: int = 1) -> List[Dict[str, Any]]:
    """
    Retrieves recent logs from Datadog filtered by field values and time range.
    """
    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours_back)
    query_str = f"@{field_filter}:{value}"
    body = build_query_body(query_str, start_time, now)
    configuration = get_datadog_configuration()
    with ApiClient(configuration) as api_client:
        api_instance = LogsQueryApi(api_client)
        response = api_instance.query(body=body)
    return parse_log_response(response.data)
