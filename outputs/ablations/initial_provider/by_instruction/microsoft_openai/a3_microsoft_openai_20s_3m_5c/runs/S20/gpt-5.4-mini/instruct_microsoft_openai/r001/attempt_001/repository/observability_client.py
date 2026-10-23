import os
from datetime import datetime, timedelta, timezone
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.monitor.query import LogsQueryClient
from azure.monitor.ingestion import LogsIngestionClient

from observability_models import LogQueryResult, LogQueryWindow, LogWriteResult, normalize_event


def _workspace_id() -> str:
    value = os.getenv("AZURE_MONITOR_WORKSPACE_ID") or os.getenv("APPLICATIONINSIGHTS_WORKSPACE_ID")
    if not value:
        raise ValueError("AZURE_MONITOR_WORKSPACE_ID is required")
    return value


def _dce_endpoint() -> str:
    value = os.getenv("AZURE_MONITOR_DCE_ENDPOINT")
    if not value:
        raise ValueError("AZURE_MONITOR_DCE_ENDPOINT is required")
    return value


def _rule_id() -> str:
    value = os.getenv("AZURE_MONITOR_DCR_IMMUTABLE_ID") or os.getenv("AZURE_MONITOR_DCR_ID")
    if not value:
        raise ValueError("AZURE_MONITOR_DCR_IMMUTABLE_ID is required")
    return value


def _credential() -> AzureKeyCredential:
    key = os.getenv("AZURE_MONITOR_DCR_STREAMING_KEY") or os.getenv("AZURE_MONITOR_API_KEY")
    if not key:
        raise ValueError("AZURE_MONITOR_DCR_STREAMING_KEY is required")
    return AzureKeyCredential(key)


def ingestion_client() -> LogsIngestionClient:
    return LogsIngestionClient(endpoint=_dce_endpoint(), credential=_credential())


def query_client() -> LogsQueryClient:
    return LogsQueryClient(credential=_credential())


def write_log_record(record: dict[str, Any], stream_name: str = "Custom-ObservabilityLogs") -> LogWriteResult:
    client = ingestion_client()
    payload = normalize_event(record)
    response = client.upload(rule_id=_rule_id(), stream_name=stream_name, logs=[payload])
    return LogWriteResult(status="submitted", request_id=getattr(response, "request_id", None), raw=response)


def query_logs(query: str, *, start_time: datetime | None = None, end_time: datetime | None = None, workspace_id: str | None = None) -> LogQueryResult:
    client = query_client()
    start = start_time or datetime.now(timezone.utc) - timedelta(hours=24)
    end = end_time or datetime.now(timezone.utc)
    result = client.query_workspace(workspace_id or _workspace_id(), query, timespan=(start, end))
    rows: list[dict[str, Any]] = []
    tables = getattr(result, "tables", []) or []
    for table in tables:
        cols = [c.name for c in table.columns]
        for row in table.rows:
            rows.append({k: v for k, v in zip(cols, row)})
    return LogQueryResult(items=rows, raw=result)


def time_window(hours: int = 24) -> LogQueryWindow:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    return LogQueryWindow(start_time=start.isoformat().replace("+00:00", "Z"), end_time=end.isoformat().replace("+00:00", "Z"))
