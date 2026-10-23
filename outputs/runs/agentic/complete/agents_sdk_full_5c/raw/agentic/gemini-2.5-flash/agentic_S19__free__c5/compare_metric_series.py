from google.cloud import monitoring_v3
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

def compare_metric_series(project_id: str, metric_type: str, end_time_iso: str, duration_seconds: int, filter_a: dict, filter_b: dict):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_dt = datetime.datetime.fromisoformat(end_time_iso.replace('Z', '+00:00'))
    end_time_timestamp = Timestamp()
    end_time_timestamp.FromDatetime(end_dt)

    start_time_timestamp = Timestamp()
    start_dt = end_dt - datetime.timedelta(seconds=duration_seconds)
    start_time_timestamp.FromDatetime(start_dt)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time_timestamp,
        start_time=start_time_timestamp,
    )

    def _build_filter(metric_type_val, filter_dict):
        filter_parts = [f'metric.type = "{metric_type_val}"']
        for key, value in filter_dict.items():
            filter_parts.append(f'{key} = "{value}"')
        return " AND ".join(filter_parts)

    results_a = client.list_time_series(
        request={
            "name": project_name,
            "filter": _build_filter(metric_type, filter_a),
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    results_b = client.list_time_series(
        request={
            "name": project_name,
            "filter": _build_filter(metric_type, filter_b),
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    
    def _extract_series_data(results, identifier):
        series_data = []
        for series in results:
            if series.points:
                value = next(iter(series.points[0].value.values())) if series.points[0].value else None
                series_data.append({
                    "identifier": identifier,
                    "metric": dict(series.metric),
                    "resource": dict(series.resource),
                    "latest_value": value,
                })
        return series_data

    return {
        "series_a": _extract_series_data(results_a, "A"),
        "series_b": _extract_series_data(results_b, "B"),
    }
