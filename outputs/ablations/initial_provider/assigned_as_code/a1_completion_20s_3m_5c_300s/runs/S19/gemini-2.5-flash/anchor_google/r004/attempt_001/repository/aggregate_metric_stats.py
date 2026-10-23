from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import normalize_time_series_response

def aggregate_metric_stats(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("project_id")
    if not project_id:
        raise ValueError("project_id must be provided in config")

    client = ObservabilityClient(project_id)
    
    time_series_list = client.list_time_series(
        metric_type=payload["metric"],
        start_time=int(payload["start_time"]),
        end_time=int(payload["end_time"]),
        interval_seconds=config.get("period_seconds", 60),
        aligner=monitoring_v3.Aggregation.Aligner[payload.get("aligner", "ALIGN_MEAN").upper()],
        reducer=monitoring_v3.Aggregation.Reducer[payload.get("reducer", "REDUCE_MEAN").upper()],
        group_by=payload.get("group_by_fields", [])
    )
    
    return {"aggregated_points": normalize_time_series_response(time_series_list)}
