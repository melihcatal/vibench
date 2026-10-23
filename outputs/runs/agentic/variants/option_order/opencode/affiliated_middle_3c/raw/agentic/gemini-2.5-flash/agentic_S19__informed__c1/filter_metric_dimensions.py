import os
from datetime import datetime, timedelta
from typing import Dict, List
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricDatapoint, MetricSeries


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    dimensions: Dict[str, str],
    minutes_ago: int = 5,
) -> List[MetricSeries]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = (now - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")

    interval = monitoring_v3.TimeInterval(
        end_time={
            "seconds": int(
                datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
            )
        },
        start_time={
            "seconds": int(
                datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
            )
        },
    )

    dimension_filter = " AND ".join(
        [f'resource.labels.{k} = "{v}"' for k, v in dimensions.items()]
    )
    metric_filter = f'metric.type = "{metric_type}" AND {dimension_filter}'

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=[
            "resource.labels.instance_name",
            "resource.type",
            "metric.labels.state",
        ],
    )

    results = client.list_time_series(
        name=project_name,
        filter=metric_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    series_list = []
    for series in results:
        datapoints = []
        for point in series.points:
            value = (
                point.value.double_value
                or point.value.int6_4_value
                or point.value.bool_value
            )
            datapoints.append(
                MetricDatapoint(timestamp=str(point.interval.end), value=value)
            )
        series_list.append(
            MetricSeries(
                metric=dict(series.metric.labels),
                resource=dict(series.resource.labels),
                points=datapoints,
            )
        )
    return series_list
