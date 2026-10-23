from __future__ import annotations

from typing import List

from observability_client import CloudWatchObservabilityClient
from observability_models import LogQueryResult



def fetch_recent_logs(
    field_name: str,
    field_value: str,
    minutes: int = 15,
    limit: int = 100,
) -> List[LogQueryResult]:
    client = CloudWatchObservabilityClient()
    safe_field_name = "".join(ch for ch in field_name if ch.isalnum() or ch in {"_", "@"})
    escaped_value = field_value.replace('"', '\\"')
    query = f'''
fields @timestamp, @message, severity, service, correlation_id, {safe_field_name}
| filter {safe_field_name} = "{escaped_value}"
| sort @timestamp desc
| limit {int(limit)}
'''.strip()
    query_id = client.start_query(query_string=query, minutes=minutes)
    return client.wait_for_query_results(query_id)
