import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI

from observability_models import LogQueryResult, LogWriteResult, normalize_event


def get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def write_log_event(event: Dict[str, Any], model: str = 'gpt-5.4-mini') -> LogWriteResult:
    client = get_client()
    payload = normalize_event(event)
    response = client.responses.create(
        model=model,
        input=[
            {
                'role': 'user',
                'content': f'Persist this structured log event for observability ingestion: {payload}',
            }
        ],
    )
    return LogWriteResult(status='submitted', raw=response.model_dump())


def query_logs(filters: Dict[str, Any], model: str = 'gpt-5.4-mini') -> LogQueryResult:
    client = get_client()
    response = client.responses.create(
        model=model,
        input=[
            {
                'role': 'user',
                'content': f'Query managed logs with filters: {filters}',
            }
        ],
    )
    raw = response.model_dump()
    return LogQueryResult(items=raw.get('output', []), raw=raw)
