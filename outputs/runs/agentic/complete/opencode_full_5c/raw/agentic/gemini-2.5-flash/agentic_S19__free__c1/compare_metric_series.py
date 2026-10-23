import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3


def compare_metric_series(
    project_id: str, metric_type: str, window_minutes: int, filter1: dict, filter2: dict
):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    def _build_filter_string(base_filter: str, dimensions: dict):
        current_filter = base_filter
        for key, value in dimensions.items():
            current_filter += f' AND metric.labels.{key} = "{value}"'
        return current_filter

    filter_string1 = _build_filter_string(f'metric.type = "{metric_type}"', filter1)
    filter_string2 = _build_filter_string(f'metric.type = "{metric_type}"', filter2)

    series1_params = {
        "name": project_name,
        "filter": filter_string1,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
    series2_params = {
        "name": project_name,
        "filter": filter_string2,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results1 = client.list_time_series(request=series1_params)
    results2 = client.list_time_series(request=series2_params)

    return {
        "series1": [monitoring_v3.TimeSeries.to_dict(series) for series in results1],
        "series2": [monitoring_v3.TimeSeries.to_dict(series) for series in results2],
    }
