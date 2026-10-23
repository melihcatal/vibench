import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from openai import AzureOpenAI

from observability_models import LogEvent, LogQueryRequest, normalize_events


def _require(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise ValueError(name)
    return value


def _client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=_require("AZURE_OPENAI_ENDPOINT"),
        api_key=_require("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )


def get_log_store_name() -> str:
    return os.getenv("AZURE_OPENAI_LOG_STORE", "managed-log-store")


def ingest_log_event(event: LogEvent) -> Dict[str, Any]:
    client = _client()
    payload = event.to_dict()
    response = client.responses.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "gpt-4.1-mini"),
        input=[{"role": "user", "content": payload["message"]}],
        metadata={"log_store": get_log_store_name(), "event": str(payload)},
    )
    return {"provider": "azure-openai", "event": payload, "response_id": response.id}


def query_logs(request: LogQueryRequest) -> List[Dict[str, Any]]:
    client = _client()
    response = client.responses.create(
        model=os.getenv("AZURE_OPENAI_QUERY_MODEL", "gpt-4.1"),
        input=[{"role": "user", "content": str(request.to_dict())}],
        metadata={"log_store": get_log_store_name(), "query": str(request.to_dict())},
    )
    rows = [{"response_id": response.id, "matched": True, "query": request.to_dict()}]
    return normalize_events(rows)


def recent_window(minutes: int = 15) -> Dict[str, datetime]:
    end = datetime.utcnow()
    start = end.fromtimestamp(end.timestamp() - minutes * 60)
    return {"start": start, "end": end}
