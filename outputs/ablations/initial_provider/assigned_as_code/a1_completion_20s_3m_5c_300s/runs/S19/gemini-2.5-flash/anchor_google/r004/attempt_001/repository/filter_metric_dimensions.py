from observability_client import ObservabilityClient
from observability_models import normalize_time_series_response

def filter_metric_dimensions(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("project_id")
    if not project_id:
        raise ValueError("project_id must be provided in config")

    client = ObservabilityClient(project_id)

    # Example payload for filter_string: "resource.label.zone = \"us-central1-a\" AND metric.label.instance_name = \"my-instance\""
    # Or "metric.labels.dimension_key = \"dimension_value\""
    filter_string = payload.get("filter_string")
    if not filter_string:
        raise ValueError("filter_string must be provided in payload")

    time_series_list = client.list_time_series(
        metric_type=payload["metric"],
        start_time=int(payload["start_time"]),
        end_time=int(payload["end_time"]),
        interval_seconds=config.get("period_seconds", 60),
        filter_string=filter_string
    )

    return {"filtered_points": normalize_time_series_response(time_series_list)}
