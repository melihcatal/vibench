from observability_client import ObservabilityClient
from observability_models import LogQueryRequest


def main():
    client = ObservabilityClient()
    query = LogQueryRequest(
        severity="error",
        start_time="2026-04-21T00:00:00Z",
        end_time="2026-04-21T23:59:59Z",
        limit=50,
    )
    return client.query_logs(query)
