from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from typing import List
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest, MetricDatapoint, MetricQueryResult

def filter_metric_dimensions(request: MetricQueryRequest) -> MetricQueryResult:
    client = ObservabilityClient()
    project_id = client.google_project_id

    # Convert ISO 8601 strings to datetime objects
    start_time_dt = datetime.fromisoformat(request.start_time)
    end_time_dt = datetime.fromisoformat(request.end_time)

    # Create a time interval
    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time_dt.timestamp())},
        start_time={'seconds': int(start_time_dt.timestamp())}
    )

    # Construct the filter string based on metric name and dimensions
    metric_filter = f'metric.type = "custom.googleapis.com/{request.metric_name}"'
    if request.dimensions:
        dimension_filters = []
        for key, value in request.dimensions.items():
            dimension_filters.append(f'metric.labels.{key} = "{value}"')
        metric_filter += ' AND ' + ' AND '.join(dimension_filters)

    results = client.monitoring_client.list_time_series(
        name=f"projects/{project_id}",
        filter=metric_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    datapoints = []
    for series in results:
        for point in series.points:
            timestamp = datetime.fromtimestamp(point.interval.end_time.seconds).isoformat()
            value = point.value.double_value if point.value.HasField('double_value') else point.value.int64_value
            dimensions = {k: v for k, v in series.metric.labels.items()}
            datapoints.append(MetricDatapoint(timestamp=timestamp, value=float(value), dimensions=dimensions))

    return MetricQueryResult(
        metric_name=request.metric_name,
        datapoints=datapoints
    )
