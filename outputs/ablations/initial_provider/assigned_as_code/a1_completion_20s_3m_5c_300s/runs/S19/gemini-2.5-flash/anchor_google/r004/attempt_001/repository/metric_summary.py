from observability_client import ObservabilityClient
from observability_models import normalize_time_series_response

def metric_summary(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("project_id")
    if not project_id:
        raise ValueError("project_id must be provided in config")

    client = ObservabilityClient(project_id)

    metric_type = payload["metric"]
    start_time = int(payload["start_time"])
    end_time = int(payload["end_time"])
    interval_seconds = config.get("period_seconds", 60)
    filter_string = payload.get("filter_string")

    time_series_list = client.list_time_series(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        interval_seconds=interval_seconds,
        filter_string=filter_string
    )

    normalized_data = normalize_time_series_response(time_series_list)

    # For a basic summary, we can just return the normalized data.
    # More advanced summary logic (e.g., anomaly detection, trend analysis) would go here.
    return {"summary_data": normalized_data}
