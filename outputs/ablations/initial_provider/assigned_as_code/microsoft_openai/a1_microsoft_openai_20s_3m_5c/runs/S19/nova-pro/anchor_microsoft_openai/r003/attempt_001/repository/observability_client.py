from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def get_metrics_query_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential)


def normalize_metric_payload(payload):
    payload['start_time'] = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    payload['end_time'] = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    return payload