from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Iterable, List

from google.cloud import logging_v2

from observability_models import LogQueryRequest, StructuredLogEvent, normalize_gcp_entries


def get_gcp_logging_client() -> logging_v2.Client:
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    if project:
        return logging_v2.Client(project=project)
    return logging_v2.Client()


def get_log_name() -> str:
    return os.getenv("GCP_LOG_NAME", "application-events")


def write_log_events(events: Iterable[StructuredLogEvent]) -> List[dict]:
    client = get_gcp_logging_client()
    logger = client.logger(get_log_name())
    written: List[dict] = []
    for event in events:
        entry = event.to_gcp_entry()
        logger.log_struct(
            entry["json_payload"],
            severity=entry["severity"],
            labels=entry["labels"],
        )
        written.append(entry)
    return written


def list_log_entries(query: LogQueryRequest):
    client = get_gcp_logging_client()
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=query.minutes)
    time_clause = f'timestamp>="{cutoff.isoformat()}"'
    filter_parts = [f'logName="projects/{client.project}/logs/{get_log_name()}"', time_clause]
    user_filter = query.build_filter()
    if user_filter:
        filter_parts.append(user_filter)
    filter_expression = " AND ".join(filter_parts)
    return client.list_entries(filter_=filter_expression, order_by=logging_v2.DESCENDING, page_size=query.limit)


def fetch_normalized_entries(query: LogQueryRequest):
    return normalize_gcp_entries(list_log_entries(query))
