# filter_metric_dimensions.py
# Queries metric data filtered by resource labels or dimensions

from observability_client import ObservabilityClient
from observability_models import MetricRequest, MetricResponse


def filter_metric_dimensions(
    service: str,
    metric: str,
    dimensions: dict,
    start: str,
    end: str,
    window: str = None,
) -> MetricResponse:
    """Return datapoints for a metric filtered by the supplied dimension key/value pairs."""
    client = ObservabilityClient.get_client(service)
    if client["service"] == "datadog":
        import requests

        api = f"https://api.datadoghq.com/api/v1/query"
        headers = {
            "DD-API-KEY": client["api_key"],
            "DD-APPLICATION-KEY": client["app_key"],
        }
        query = f"{metric}{{service:{service}}}"  # base query
        # Add each dimension as a filter
        for key, value in dimensions.items():
            query += f":{key}:{value}"
        payload = {"from": start, "to": end, "query": query, "interval": window or "1h"}
        resp = requests.get(api, headers=headers, params=payload)
        resp.raise_for_status()
        raw = resp.json()
        datapoints = [(pt["timestamp"], pt["value"]) for pt in raw["series"]]
        return MetricResponse(
            service, metric, datapoints, metadata={"filters": dimensions}
        )
    elif client["service"] == "google":
        from google.cloud import monitoring_v3

        client = monitoring_v3.MetricServiceClient()
        project = client.project_path(client.project)
        filter_expr = f'metric.type = "custom.googleapis.com/{metric}"'
        for key, value in dimensions.items():
            filter_expr += f' AND resource.label.{key} = "{value}"'
        series = client.list_time_series(
            request={
                "name": project,
                "filter": filter_expr,
                "interval": {
                    "start_time": {"seconds": int(start)},
                    "end_time": {"seconds": int(end)},
                },
            }
        )
        datapoints = [
            (p.interval.start_time.seconds, float(p.value.double_value)) for p in series
        ]
        return MetricResponse(
            service, metric, datapoints, metadata={"filter_labels": dimensions}
        )
    elif client["service"] == "aws":
        import boto3

        cw = boto3.client("cloudwatch", region_name="us-east-1")
        resp = cw.get_metric_statistics(
            Namespace=metric,  # placeholder namespace
            MetricName=metric,
            Dimensions=[{"Name": k, "Value": v} for k, v in dimensions.items()],
            StartTime=int(start),
            EndTime=int(end),
            Period=3600,
            Statistics=["Average"],
        )
        stats = resp["Datapoints"][0]
        return MetricResponse(
            service, metric, [], metadata={"dimension_filters": dimensions}
        )
    else:
        raise ValueError(f"Unsupported service for filter_metric_dimensions: {service}")
