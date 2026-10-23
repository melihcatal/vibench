from observability_client import DatadogLogsClient
from observability_models import LogQuery


def fetch_recent_logs(field_name, field_value, start_time=None, end_time=None):
    client = DatadogLogsClient()
    query = LogQuery(
        query=f"{field_name}:{field_value}", start_time=start_time, end_time=end_time
    )
    return client.query_logs(query)
