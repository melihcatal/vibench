import os
from datetime import datetime, timedelta
from google.cloud.monitoring_v3.types import TimeInterval, Aggregation
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client
from observability_models import AggregatedMetricData


def get_aggregated_metric(
    project_id: str,
    metric_name: str,
    minutes_ago: int = 60,
    aggregator: str = "ALIGN_MEAN",
) -> list[AggregatedMetricData]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)

    start_timestamp = Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = Timestamp()
    end_timestamp.FromDatetime(now)

    interval = TimeInterval(start_time=start_timestamp, end_time=end_timestamp)

    aggregation = Aggregation(
        alignment_period={"seconds": minutes_ago * 60},
        per_series_aligner=Aggregation.Aligner[aggregator],
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_name}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    output = []
    for result in results:
        if result.points:
            point = result.points[0]
            output.append(
                AggregatedMetricData(
                    metric_name=result.metric.type,
                    aggregation=aggregator,
                    value=point.value.double_value,
                    time_window={
                        "start": point.interval.start_time.isoformat(),
                        "end": point.interval.end_time.isoformat(),
                    },
                )
            )
    return output


if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    aggregated_data = get_aggregated_metric(
        project, metric_type, minutes_ago=30, aggregator="ALIGN_MAX"
    )
    for data in aggregated_data:
        print(f"Metric: {data.metric_name}")
        print(f"Aggregation: {data.aggregation}")
        print(f"Value: {data.value}")
        print(f"Time Window: {data.time_window}")
