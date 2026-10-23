from observability_client import ObservabilityClient
from observability_models import normalize_time_series_response

def compare_metric_series(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("project_id")
    if not project_id:
        raise ValueError("project_id must be provided in config")

    client = ObservabilityClient(project_id)

    metric_type = payload["metric"]
    start_time = int(payload["start_time"])
    end_time = int(payload["end_time"])
    interval_seconds = config.get("period_seconds", 60)

    filter_string_1 = payload.get("filter_string_1")
    filter_string_2 = payload.get("filter_string_2")

    if not filter_string_1 or not filter_string_2:
        raise ValueError("Both filter_string_1 and filter_string_2 must be provided in payload")

    time_series_list_1 = client.list_time_series(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        interval_seconds=interval_seconds,
        filter_string=filter_string_1
    )

    time_series_list_2 = client.list_time_series(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        interval_seconds=interval_seconds,
        filter_string=filter_string_2
    )

    return {
        "series_1": normalize_time_series_response(time_series_list_1),
        "series_2": normalize_time_series_response(time_series_list_2)
    }
