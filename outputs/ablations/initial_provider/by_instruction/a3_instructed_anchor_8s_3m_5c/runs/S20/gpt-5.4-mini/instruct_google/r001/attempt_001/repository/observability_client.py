import os
from typing import Any, Dict, List, Optional

from google.cloud import logging_v2

from observability_models import LogEntryView, LogQuery, build_structured_log_payload


def get_project_id() -> str:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GCLOUD_PROJECT')
    if not project_id:
        raise ValueError('GOOGLE_CLOUD_PROJECT is required')
    return project_id


def get_logging_client() -> logging_v2.Client:
    return logging_v2.Client(project=get_project_id())


def write_structured_event(message: str, severity: str = 'INFO', **fields: Any) -> Dict[str, Any]:
    client = get_logging_client()
    logger = client.logger(os.getenv('GOOGLE_CLOUD_LOG_NAME', 'application'))
    payload = build_structured_log_payload(message, severity, **fields)
    logger.log_struct(payload, severity=severity)
    return payload


def query_log_entries(query: LogQuery) -> List[Dict[str, Any]]:
    client = get_logging_client()
    results = client.list_entries(filter_=query.filter_expression, page_size=query.page_size, project_ids=[query.project_id])
    output: List[Dict[str, Any]] = []
    for entry in results:
        output.append({
            'timestamp': getattr(entry, 'timestamp', None).isoformat() if getattr(entry, 'timestamp', None) else None,
            'severity': getattr(entry, 'severity', None),
            'message': getattr(entry, 'payload', None).get('message') if isinstance(getattr(entry, 'payload', None), dict) else getattr(entry, 'text_payload', None),
            'labels': dict(getattr(entry, 'labels', {}) or {}),
        })
    return output


def build_time_range_filter(severity: Optional[str] = None, field_filters: Optional[Dict[str, str]] = None, hours: int = 24) -> str:
    parts = [f'timestamp >= "-P{hours}H"']
    if severity:
        parts.append(f'severity>={severity}')
    for key, value in (field_filters or {}).items():
        parts.append(f'{key}="{value}"')
    return ' AND '.join(parts)
