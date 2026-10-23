from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def compare_metric_series(project_id: str, metric_type: str, filter_set_1: dict, filter_set_2: dict, minutes_ago: int = 60):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    def _get_time_series_data(filters: dict):
        filter_string = ""
        for key, value in filters.items():
            filter_string += f'metric.labels.{key} = "{value}" AND '
        if filter_string:
            filter_string = filter_string[:-5]
        
        query = f"fetch gce_instance | metric {metric_type} | filter {filter_string} | within {minutes_ago}m"
        results = client.query_time_series(
            name=project_name,
            query=query,
            interval=interval,
        )

        time_series_data = []
        for time_series in results:
            for point in time_series.points:
                time_series_data.append({
                    "metric": time_series.metric.type,
                    "value": point.value.double_value,
                    "timestamp": point.interval.end_time.timestamp(),
                    "resource": {
                        "type": time_series.resource.type,
                        "labels": dict(time_series.resource.labels)
                    }
                })
        return time_series_data

    data_series_1 = _get_time_series_data(filter_set_1)
    data_series_2 = _get_time_series_data(filter_set_2)

    return {
        "series_1": {
            "filter": filter_set_1,
            "data": data_series_1
        },
        "series_2": {
            "filter": filter_set_2,
            "data": data_series_2
        }
    }
