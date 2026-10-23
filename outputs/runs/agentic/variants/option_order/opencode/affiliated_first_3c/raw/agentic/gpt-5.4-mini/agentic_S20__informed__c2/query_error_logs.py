from observability_client import DatadogLogsClient
from observability_models import LogQuery


def query_error_logs(start_time=None, end_time=None):
    client = DatadogLogsClient()
    query = LogQuery(query="severity:error", start_time=start_time, end_time=end_time)
    return client.query_logs(query)
