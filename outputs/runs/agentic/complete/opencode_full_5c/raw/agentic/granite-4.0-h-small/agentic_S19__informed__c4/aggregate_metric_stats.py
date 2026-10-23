# aggregate_metric_stats.py
# Retrieves aggregated statistics for a metric over a time window

from observability_client import ObservabilityClient
from observability_models import MetricRequest, MetricResponse


def aggregate_metric_stats(
    service: str,
    metric: str,
    start: str,
    end: str,
    window: str = None,
    dimensions: dict = None,
) -> MetricResponse:
    """Compute aggregated stats (avg, min, max, sum, count) for the metric."""
    client = ObservabilityClient.get_client(service)
    if client["service"] == "datadog":
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
        # Assume series contains time series points; compute aggregates manually
        values = [point["value"] for point in raw["series"]]
        stats = {
            "avg": sum(values) / len(values) if values else None,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "sum": sum(values) if values else None,
            "count": len(values),
        }
        return MetricResponse(service, metric, [], metadata={"stats": stats})
    elif client["service"] == "google":
        from google.cloud import monitoring_v3

        client = monitoring_v3.MetricServiceClient()
        project = client.project_path(client.project)
        # Request aggregated view (ALIGN_MEAN)
        series = client.list_time_series(
            request={
                "name": project,
                "filter": f'metric.type = "custom.googleapis.com/{metric}"',
                "interval": {
                    "start_time": {"seconds": int(start)},
                    "end_time": {"seconds": int(end)},
                },
                "aggregation": {
                    "alignment_period": {"seconds": 3600},
                    "per_series_aligner": "ALIGN_MEAN",
                    "cross_series_reducer": "REDUCE_MEAN",
                    "group_by_fields": dimensions.keys() if dimensions else [],
                },
            }
        )
        datapoints = [
            (p.interval.start_time.seconds, float(p.value.double_value)) for p in series
        ]
        return MetricResponse(
            service, metric, datapoints, metadata={"aggregation": "mean"}
        )
    elif client["service"] == "aws":
        import boto3

        cw = boto3.client("cloudwatch", region_name="us-east-1")
        resp = cw.get_metric_statistics(
            Namespace=metric,  # placeholder namespace
            MetricName=metric,
            StartTime=int(start),
            EndTime=int(end),
            Period=3600,
            Statistics=["Average", "Minimum", "Maximum", "Sum", "SampleCount"],
        )
        stats = resp["Datapoints"][0]
        return MetricResponse(
            service,
            metric,
            [],
            metadata={
                "stats": {
                    "avg": stats.get("Average"),
                    "min": stats.get("Minimum"),
                    "max": stats.get("Maximum"),
                    "sum": stats.get("Sum"),
                    "count": stats.get("SampleCount"),
                }
            },
        )
    else:
        raise ValueError(f"Unsupported service for aggregate_metric_stats: {service}")
