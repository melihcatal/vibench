from google.cloud import monitoring_v3
from datetime import datetime, timedelta
import google.api_core.exceptions

def query_metric_window(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    time_window_minutes: int,
):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=time_window_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())}
    )

    query_filter = f'metric.type = "{metric_type}"'

    try:
        response = client.list_time_series(
            name=project_name,
            filter=query_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series_data = []
        for series in response:
            for point in series.points:
                time_series_data.append({
                    "timestamp": point.interval.end_time.timestamp(),
                    "value": point.value.double_value if point.value.HasField("double_value") else point.value.int64_value
                })
        return time_series_data
    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Error querying metric: {e}")
        return None
