from observability_client import ObservabilityClient


def metric_summary(metric_name: str, start_time: str, end_time: str):
    client = ObservabilityClient()
    return client.post("/metrics/summary", {"metricName": metric_name, "startTime": start_time, "endTime": end_time, "model": "openai/gpt-5.4-mini"})
