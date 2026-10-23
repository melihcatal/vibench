from __future__ import annotations

from typing import List

from observability_client import CloudWatchObservabilityClient
from observability_models import LogQueryResult



def query_error_logs(minutes: int = 30, limit: int = 50) -> List[LogQueryResult]:
    client = CloudWatchObservabilityClient()
    query = f'''
fields @timestamp, @message, severity, service, correlation_id
| filter severity = "ERROR"
| sort @timestamp desc
| limit {int(limit)}
'''.strip()
    query_id = client.start_query(query_string=query, minutes=minutes)
    return client.wait_for_query_results(query_id)
