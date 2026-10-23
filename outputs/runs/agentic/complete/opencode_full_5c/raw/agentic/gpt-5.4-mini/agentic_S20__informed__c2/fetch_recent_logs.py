from observability_client import DatadogObservabilityClient, default_time_window
from observability_models import QueryRequest


def fetch_recent_logs() -> object:
    client = DatadogObservabilityClient()
    start_time, end_time = default_time_window(10)
    request = QueryRequest(
        start_time=start_time,
        end_time=end_time,
        field_filters={"env": "production", "service": "checkout-service"},
        limit=25,
    )
    return client.query_logs(request)
