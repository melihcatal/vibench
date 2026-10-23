from datetime import datetime, timedelta, timezone
from typing import Dict, List
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricTimeSeries, MetricDataPoint
from google.cloud import monitoring_v3


def _fetch_series(client, project_name, filter_str, interval):
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    time_series_list = []
    for result in results:
        points = [
            MetricDataPoint(
                timestamp=p.interval.end_time.rfc3339(), value=p.value.double_value
            )
            for p in result.points
        ]
        ts = MetricTimeSeries(
            metric_kind=str(result.metric_kind),
            value_type=str(result.value_type),
            metric_labels=dict(result.metric.labels),
            resource_labels=dict(result.resource.labels),
            points=points,
        )
        time_series_list.append(ts)
    return time_series_list


def compare_metric_series(
    project_id: str,
    metric_type: str,
    minutes_ago: int,
    filter1: Dict[str, str],
    filter2: Dict[str, str],
) -> Dict[str, List[MetricTimeSeries]]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(now.timestamp())},
        }
    )

    filter1_str = f'metric.type = "{metric_type}"'
    for key, value in filter1.items():
        filter1_str += f' AND {key} = "{value}"'

    filter2_str = f'metric.type = "{metric_type}"'
    for key, value in filter2.items():
        filter2_str += f' AND {key} = "{value}"'

    series1 = _fetch_series(client, project_name, filter1_str, interval)
    series2 = _fetch_series(client, project_name, filter2_str, interval)

    return {"series1": series1, "series2": series2}


if __name__ == "__main__":
    project = get_project_id()
    metric = "compute.googleapis.com/instance/network/received_bytes_count"
    # Compare two different instance zones
    f1 = {"resource.label.zone": "us-central1-a"}
    f2 = {"resource.label.zone": "us-east1-b"}

    comparison = compare_metric_series(project, metric, 30, f1, f2)
    print("--- Series 1 (us-central1-a) ---")
    for ts in comparison["series1"]:
        print(ts)
    print("\n--- Series 2 (us-east1-b) ---")
    for ts in comparison["series2"]:
        print(ts)
