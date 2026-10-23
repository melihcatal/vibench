import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from openai import OpenAI

from observability_models import LogQuery, StructuredLogEvent, normalize_results


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def default_service() -> str:
    return os.environ.get("OBSERVABILITY_SERVICE", "managed-log-query")


def write_log(event: StructuredLogEvent) -> Dict[str, Any]:
    payload = event.to_dict()
    client = _client()
    response = client.responses.create(model="gpt-5.4-mini", input=[{"role": "system", "content": "Persist this structured log event as JSON."}, {"role": "user", "content": str(payload)}])
    return {"provider": "openai", "model": "gpt-5.4-mini", "request": payload, "response_id": response.id}


def query_logs(query: LogQuery) -> List[Dict[str, Any]]:
    client = _client()
    response = client.responses.create(model="gpt-5.4-mini", input=[{"role": "system", "content": "Return recent log entries matching the filter as JSON array."}, {"role": "user", "content": str(query.to_dict())}])
    return normalize_results([{"query": query.to_dict(), "response_id": response.id, "provider": "openai", "model": "gpt-5.4-mini"}])


def recent_time_range(minutes: int = 60) -> Dict[str, str]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    return {"start_time": start_time.isoformat(), "end_time": end_time.isoformat()}
