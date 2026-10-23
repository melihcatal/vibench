from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient
from azure.core.credentials import AzureKeyCredential

from observability_models import LogEvent, LogQueryRequest, normalize_log_event, normalize_time_range


@dataclass(frozen=True)
class ObservabilityConfig:
    dce_endpoint: str
    dcr_immutable_id: str
    stream_name: str
    workspace_id: str

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        dce_endpoint = os.environ.get("AZURE_MONITOR_DCE_ENDPOINT", "").strip()
        dcr_immutable_id = os.environ.get("AZURE_MONITOR_DCR_IMMUTABLE_ID", "").strip()
        stream_name = os.environ.get("AZURE_MONITOR_STREAM_NAME", "Custom-LogEvents").strip()
        workspace_id = os.environ.get("AZURE_MONITOR_WORKSPACE_ID", "").strip()
        return cls(
            dce_endpoint=dce_endpoint,
            dcr_immutable_id=dcr_immutable_id,
            stream_name=stream_name,
            workspace_id=workspace_id,
        )


def build_ingestion_client() -> LogsIngestionClient:
    endpoint = os.environ["AZURE_MONITOR_DCE_ENDPOINT"]
    credential = AzureKeyCredential(os.environ["AZURE_MONITOR_DATA_COLLECTION_RULE_KEY"])
    return LogsIngestionClient(endpoint=endpoint, credential=credential)


def build_query_client() -> LogsQueryClient:
    credential = AzureKeyCredential(os.environ["AZURE_MONITOR_QUERY_KEY"])
    return LogsQueryClient(credential)


def ingest_log_event(event: LogEvent) -> Dict[str, Any]:
    config = ObservabilityConfig.from_env()
    client = build_ingestion_client()
    payload = [normalize_log_event(event)]
    client.upload(rule_id=config.dcr_immutable_id, stream_name=config.stream_name, logs=payload)
    return {"stream_name": config.stream_name, "count": len(payload), "status": "submitted"}


def ingest_log_events(events: Iterable[LogEvent]) -> Dict[str, Any]:
    config = ObservabilityConfig.from_env()
    client = build_ingestion_client()
    payload = [normalize_log_event(event) for event in events]
    client.upload(rule_id=config.dcr_immutable_id, stream_name=config.stream_name, logs=payload)
    return {"stream_name": config.stream_name, "count": len(payload), "status": "submitted"}


def query_logs(request: LogQueryRequest) -> Dict[str, Any]:
    client = build_query_client()
    start, end = normalize_time_range(request.start_time, request.end_time)
    timespan = (start, end)
    query = request.query
    if request.severity:
        query = f"{query} | where Severity == '{request.severity}'" if query else f"| where Severity == '{request.severity}'"
    response = client.query_workspace(
        workspace_id=ObservabilityConfig.from_env().workspace_id,
        query=query or "",
        timespan=timespan,
    )
    tables = []
    for table in getattr(response, "tables", []) or []:
        rows = [dict(zip(table.columns, row)) for row in table.rows]
        tables.append({"name": table.name, "rows": rows})
    return {"tables": tables, "status": getattr(response, "status", None)}


def filter_result_rows(rows: List[Dict[str, Any]], field_filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    filtered = []
    for row in rows:
        if all(row.get(key) == value for key, value in field_filters.items()):
            filtered.append(row)
    return filtered
