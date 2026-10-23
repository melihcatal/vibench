import os
from typing import Any, Dict, List, Optional

from google.cloud import logging as gcloud_logging

from observability_models import LogQueryRequest, LogQueryResponse, LogWriteRequest, as_field_filters, normalize_log_entry, normalize_severity


def _project_id() -> str:
    for key in ("GOOGLE_CLOUD_PROJECT", "GCLOUD_PROJECT", "GCP_PROJECT"):
        value = os.getenv(key)
        if value:
            return value
    return ""


def create_logging_client() -> gcloud_logging.Client:
    return gcloud_logging.Client(project=_project_id() or None)


def write_json_log(request: LogWriteRequest) -> Dict[str, Any]:
    client = create_logging_client()
    logger = client.logger(request.log_name)
    payload = normalize_log_entry(request.payload, request.severity)
    logger.log_struct(payload, severity=normalize_severity(request.severity))
    return payload


def query_logs(request: LogQueryRequest, page_size: int = 50) -> LogQueryResponse:
    client = create_logging_client()
    filters = [f'logName="projects/{client.project}/logs/{request.log_name}"']
    if request.severity:
        filters.append(f'severity>={normalize_severity(request.severity)}')
    filters.append(f'timestamp>="{request.start_time}"')
    filters.append(f'timestamp<="{request.end_time}"')
    filters.extend(as_field_filters(request.filters))
    entries = list(client.list_entries(filter_=" AND ".join(filters), page_size=page_size))
    return LogQueryResponse(entries=[dict(entry) for entry in entries], next_page_token="")


def get_recent_logs(log_name: str, start_time: str, end_time: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    response = query_logs(LogQueryRequest(log_name=log_name, start_time=start_time, end_time=end_time, filters=filters))
    return response.entries
