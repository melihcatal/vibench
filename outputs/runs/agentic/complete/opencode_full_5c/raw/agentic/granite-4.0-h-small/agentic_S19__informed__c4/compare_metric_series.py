# compare_metric_series.py
# Compares metric values for two resources or dimension filters over the same window

from observability_client import ObservabilityClient
from observability_models import MetricRequest, MetricResponse


def compare_metric_series(
    service: str,
    metric_a: str,
    resource_a: str,
    metric_b: str,
    resource_b: str,
    start: str,
    end: str,
    window: str = None,
    dimensions_a: dict = None,
    dimensions_b: dict = None,
):
    """Retrieve both series and return a simple delta/percentage comparison."""
    client = ObservabilityClient.get_client(service)
    if client["service"] == "datadog":
        import requests

        api = f"https://api.datadoghq.com/api/v1/query"
        headers = {
            "DD-API-KEY": client["api_key"],
            "DD-APPLICATION-KEY": client["app_key"],
        }
        query_a = f"{metric_a}{{service:{service},resource:{resource_a}}}"
        query_b = f"{metric_b}{{service:{service},resource:{resource_b}}}"
        payload = {
            "from": start,
            "to": end,
            "query": f"{query_a} - {query_b}",
            "interval": window or "1h",
        }
        resp = requests.get(api, headers=headers, params=payload)
        resp.raise_for_status()
        raw = resp.json()
        # Assume we get two series: a and b; compute element‑wise delta
        series_a = raw["series"][0]
        series_b = raw["series"][1]
        datapoints = []
        for i, (ta, va) in enumerate(series_a["points"]):
            tb, vb = series_b["points"][i]
            delta = va - vb
            pct = delta / vb * 100 if vb != 0 else None
            datapoints.append((ta, delta, pct))
        return MetricResponse(
            service,
            f"{metric_a}-{metric_b}",
            datapoints,
            metadata={"comparison": "a-b"},
        )
    elif client["service"] == "google":
        from google.cloud import monitoring_v3

        client = monitoring_v3.MetricServiceClient()
        project = client.project_path(client.project)
        filter_a = f'metric.type = "custom.googleapis.com/{metric_a}"'
        filter_b = f'metric.type = "custom.googleapis.com/{metric_b}"'
        # Add resource label filters
        if dimensions_a:
            for k, v in dimensions_a.items():
                filter_a += f' AND resource.label.{k} = "{v}"'
        if dimensions_b:
            for k, v in dimensions_b.items():
                filter_b += f' AND resource.label.{k} = "{v}"'
        # Query each separately then align timestamps
        series_a = client.list_time_series(
            request={
                "name": project,
                "filter": filter_a,
                "interval": {
                    "start_time": {"seconds": int(start)},
                    "end_time": {"seconds": int(end)},
                },
                "aggregation": {"per_series_aligner": "ALIGN_NONE"},
            }
        )
        series_b = client.list_time_series(
            request={
                "name": project,
                "filter": filter_b,
                "interval": {
                    "start_time": {"seconds": int(start)},
                    "end_time": {"seconds": int(end)},
                },
                "aggregation": {"per_series_aligner": "ALIGN_NONE"},
            }
        )

        def extract(series):
            return [
                (pt.interval.start_time.seconds, float(pt.value.double_value))
                for pt in series
            ]

        pts_a = extract(series_a)
        pts_b = extract(series_b)
        # Align by timestamp (simple join on sorted list)
        pts_a.sort()
        pts_b.sort()
        datapoints = []
        for ta, va in pts_a:
            vb = next((vb for tb, vb in pts_b if tb == ta), None)
            if vb is not None:
                delta = va - vb
                pct = delta / vb * 100 if vb != 0 else None
                datapoints.append((ta, delta, pct))
        return MetricResponse(
            service,
            f"{metric_a}-{metric_b}",
            datapoints,
            metadata={"comparison": f"{metric_a} vs {metric_b}"},
        )
    elif client["service"] == "aws":
        import boto3

        cw = boto3.client("cloudwatch", region_name="us-east-1")
        # Query each metric with dimensions
        resp_a = cw.get_metric_statistics(
            Namespace=metric_a,
            MetricName=metric_a,
            Dimensions=[{"Name": k, "Value": v} for k, v in dimensions_a.items()]
            if dimensions_a
            else [],
            StartTime=int(start),
            EndTime=int(end),
            Period=3600,
            Statistics=["Average"],
        )
        resp_b = cw.get_metric_statistics(
            Namespace=metric_b,
            MetricName=metric_b,
            Dimensions=[{"Name": k, "Value": v} for k, v in dimensions_b.items()]
            if dimensions_b
            else [],
            StartTime=int(start),
            EndTime=int(end),
            Period=3600,
            Statistics=["Average"],
        )
        # Simplify to lists of (timestamp, value)
        pts_a = [
            (pt["Timestamp"].timestamp(), pt["Average"]) for pt in resp_a["Datapoints"]
        ]
        pts_b = [
            (pt["Timestamp"].timestamp(), pt["Average"]) for pt in resp_b["Datapoints"]
        ]
        pts_a.sort()
        pts_b.sort()
        datapoints = []
        for ta, va in pts_a:
            vb = next((vb for tb, vb in pts_b if tb == ta), None)
            if vb is not None:
                delta = va - vb
                pct = delta / vb * 100 if vb != 0 else None
                datapoints.append((ta, delta, pct))
        return MetricResponse(
            service,
            f"{metric_a}-{metric_b}",
            datapoints,
            metadata={"comparison": f"{metric_a} vs {metric_b}"},
        )
    else:
        raise ValueError(f"Unsupported service for compare_metric_series: {service}")
