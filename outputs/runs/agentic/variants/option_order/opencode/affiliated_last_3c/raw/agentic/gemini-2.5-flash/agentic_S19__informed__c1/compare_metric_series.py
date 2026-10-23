from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import create_time_interval, normalize_time_series


def compare_metric_series(
    metric_type,
    end_time_str,
    minutes,
    filter1_key,
    filter1_value,
    filter2_key,
    filter2_value,
):
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"
    interval = create_time_interval(end_time_str, minutes)

    query1 = f'metric.type="{metric_type}" AND resource.labels.{filter1_key}="{filter1_value}"'
    query2 = f'metric.type="{metric_type}" AND resource.labels.{filter2_key}="{filter2_value}"'

    result1 = client.list_time_series(
        request={
            "name": project_name,
            "filter": query1,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    normalized_data1 = normalize_time_series(result1)

    result2 = client.list_time_series(
        request={
            "name": project_name,
            "filter": query2,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    normalized_data2 = normalize_time_series(result2)

    return {"series1": normalized_data1, "series2": normalized_data2}
