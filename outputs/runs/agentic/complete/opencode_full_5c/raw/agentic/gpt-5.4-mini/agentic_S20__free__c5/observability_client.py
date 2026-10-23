import os
from typing import Any, Dict, List, Optional

from google.cloud import logging_v2
from google.cloud import logging_v2_v1

from observability_models import LogEvent, ensure_list, normalize_severity


def get_project_id() -> str:
    project_id = (
        os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCP_PROJECT")
        or os.getenv("GOOGLE_PROJECT_ID")
    )
    if not project_id:
        raise ValueError("Missing Google Cloud project id")
    return project_id


def get_logging_client() -> logging_v2.Client:
    return logging_v2.Client(project=get_project_id())


def write_log_event(event: LogEvent) -> Dict[str, Any]:
    client = get_logging_client()
    logger = client.logger(event.service)
    payload = event.to_payload()
    logger.log_struct(payload, severity=normalize_severity(event.severity))
    return payload


def query_entries(filter_expr: str, limit: int = 50) -> List[Dict[str, Any]]:
    client = get_logging_client()
    entries = client.list_entries(filter_=filter_expr, page_size=limit)
    results: List[Dict[str, Any]] = []
    for entry in entries:
        results.append(
            {
                "timestamp": getattr(entry, "timestamp", None),
                "payload": getattr(entry, "payload", None),
                "severity": getattr(entry, "severity", None),
            }
        )
    return results[:limit]


def build_time_filter(
    severity: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    field_filters: Optional[Dict[str, str]] = None,
) -> str:
    clauses = ['resource.type="global"']
    if severity:
        clauses.append(f"severity>={normalize_severity(severity)}")
    if start_time:
        clauses.append(f'timestamp>="{start_time}"')
    if end_time:
        clauses.append(f'timestamp<="{end_time}"')
    if field_filters:
        for field, value in field_filters.items():
            clauses.append(f'{field}="{value}"')
    return " AND ".join(clauses)


def recent_payloads(raw_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return ensure_list(raw_entries)
