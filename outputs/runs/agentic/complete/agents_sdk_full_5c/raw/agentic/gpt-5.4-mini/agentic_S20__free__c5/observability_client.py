from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI

from observability_models import LogEvent, QueryFilters, normalize_log_event, normalize_query_filters


@dataclass(frozen=True)
class ObservabilityConfig:
    openai_api_key: Optional[str]
    openai_base_url: Optional[str]
    log_namespace: str


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL"),
        log_namespace=os.getenv("LOG_NAMESPACE", "production-app"),
    )


def build_openai_client(config: Optional[ObservabilityConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.openai_api_key:
        kwargs["api_key"] = cfg.openai_api_key
    if cfg.openai_base_url:
        kwargs["base_url"] = cfg.openai_base_url
    return OpenAI(**kwargs)


def create_log_event_payload(event: LogEvent) -> Dict[str, Any]:
    return normalize_log_event(event)


def create_query_payload(filters: QueryFilters) -> Dict[str, Any]:
    return normalize_query_filters(filters)


def serialize_payload(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def send_structured_log(client: OpenAI, event: LogEvent) -> Dict[str, Any]:
    payload = create_log_event_payload(event)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Store this structured log event as an operational record.",
            },
            {
                "role": "user",
                "content": serialize_payload(payload),
            },
        ],
    )
    return {"provider": "openai", "payload": payload, "response_id": response.id}


def send_correlated_logs(client: OpenAI, events: Iterable[LogEvent]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for event in events:
        results.append(send_structured_log(client, event))
    return results


def query_logs(client: OpenAI, filters: QueryFilters) -> Dict[str, Any]:
    payload = create_query_payload(filters)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Return matching recent log entries as JSON."},
            {"role": "user", "content": serialize_payload(payload)},
        ],
    )
    return {"provider": "openai", "query": payload, "response_id": response.id}
