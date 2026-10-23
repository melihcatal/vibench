import boto3

from observability_models import normalize_result


def incident_summary(payload, config=None):
    client = boto3.client("logs", region_name=(config or {}).get("region"))
    response = client.filter_log_events(
        logGroupName=(config or {}).get("log_group"),
        startTime=payload["start_time"],
        endTime=payload["end_time"],
        filterPattern="error OR exception OR failure",
    )
    normalized = normalize_result(response)
    return {
        "incident_summary": {
            "count": len(normalized["items"]),
            "time_range": {"start_time": payload["start_time"], "end_time": payload["end_time"]},
        }
    }
