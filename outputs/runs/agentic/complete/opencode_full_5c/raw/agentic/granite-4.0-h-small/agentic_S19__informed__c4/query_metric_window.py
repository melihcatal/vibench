# query_metric_window.py
# Queries recent datapoints for a named metric over a time window

from observability_client import ObservabilityClient
from observability_models import MetricRequest, MetricResponse


def query_metric_window(
    service: str,
    metric: str,
    start: str,
    end: str,
    window: str = None,
    dimensions: dict = None,
) -> MetricResponse:
    """Return time‑windowed datapoints for the given metric."""
    client = ObservabilityClient.get_client(service)
    if client["service"] == "datadog":
        # Datadog REST API example (simplified)
        import requests

        api = f"https://api.datadoghq.com/api/v1/query"
        headers = {
            "DD-API-KEY": client["api_key"],
            "DD-APPLICATION-KEY": client["app_key"],
        }
        payload = {
            "from": start,
            "to": end,
            "query": f"{metric}{{service:{service}}}",
            "interval": window or "1h",
        }
        resp = requests.get(api, headers=headers, params=payload)
        resp.raise_for_status()
        raw = resp.json()
        # Convert to normalized datapoints list
        datapoints = [(point["timestamp"], point["value"]) for point in raw["series"]]
        return MetricResponse(service, metric, datapoints)
    elif client["service"] == "google":
        # Google Cloud Monitoring SDK example
        from google.cloud import monitoring_v3

        client = monitoring_v3.MetricServiceClient()
        project = client.project_path(client.project)
        series = client.list_time_series(
            request={
                "name": project,
                "filter": f'metric.type = "custom.googleapis.com/{metric}"',
                "interval": {
                    "start_time": {"seconds": int(start)},
                    "end_time": {"seconds": int(end)},
                },
                "aggregation": {
                    "per_series_aligner": "ALIGN_NONE",
                    "cross_series_reducer": "REDUCE_NONE",
                    "group_by_fields": dimensions.keys() if dimensions else [],
                },
            }
        )
        datapoints = []
        for s in series:
            for p in s.points:
                datapoints.append(
                    (p.interval.start_time.seconds, float(p.value.double_value))
                )
        return MetricResponse(
            service, metric, datapoints, metadata={"filter": f"{metric}"}
        )
    elif client["service"] == "aws":
        # AWS CloudWatch example using Boto3
        import boto3

        cw = boto3.client("cloudwatch", region_name="us-east-1")
        resp = cw.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "m1",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": metric,  # placeholder namespace
                            "MetricName": metric,
                        },
                        "Period": 3600,
                        "Stat": "Average",
                    },
                    "ReturnData": True,
                }
            ],
            StartTime=int(start),
            EndTime=int(end),
        )
        datapoints = [
            (p["Timestamp"], int(p["Sum"]))
            for p in resp["MetricDataResults"][0]["Values"]
        ]
        return MetricResponse(service, metric, datapoints)
    else:
        raise ValueError(f"Unsupported service for query_metric_window: {service}")
