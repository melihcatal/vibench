from observability_client import DatadogObservabilityClient, default_time_window
from observability_models import QueryRequest


def query_error_logs() -> object:
    client = DatadogObservabilityClient()
    start_time, end_time = default_time_window(30)
    request = QueryRequest(
        start_time=start_time,
        end_time=end_time,
        severity="error",
        field_filters={"service": "checkout-service"},
        limit=50,
    )
    return client.query_logs(request)
