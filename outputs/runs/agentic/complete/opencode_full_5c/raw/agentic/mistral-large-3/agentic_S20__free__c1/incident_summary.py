from typing import List, Dict
from datetime import datetime
from query_error_logs import query_error_logs
from observability_models import parse_datadog_log


def summarize_error_logs_for_incident(
    service_name: str, hours_back: int = 24
) -> Dict[str, Any]:
    """
    Summarizes error log findings from Datadog for incident review.

    Args:
        service_name: Name of the service to analyze
        hours_back: Time range in hours to look back

    Returns:
        Dictionary containing incident summary with error counts, samples, and trends
    """
    error_logs = query_error_logs(
        service_name=service_name,
        min_severity="ERROR",
        hours_back=hours_back,
        limit=1000,
    )

    if not error_logs:
        return {
            "status": "no_errors",
            "message": "No errors found in the specified time range",
        }

    # Parse and normalize logs
    parsed_logs = [parse_datadog_log(log) for log in error_logs]

    # Group by error type
    error_groups = {}
    for log in parsed_logs:
        error_type = log.get("error_type", "unknown")
        if error_type not in error_groups:
            error_groups[error_type] = []
        error_groups[error_type].append(log)

    # Generate summary
    summary = {
        "service": service_name,
        "time_range": {
            "from": (datetime.utcnow() - timedelta(hours=hours_back)).isoformat() + "Z",
            "to": datetime.utcnow().isoformat() + "Z",
        },
        "total_errors": len(parsed_logs),
        "unique_error_types": len(error_groups),
        "error_distribution": {k: len(v) for k, v in error_groups.items()},
        "sample_errors": {k: v[:3] for k, v in error_groups.items()},
        "trends": {
            "recent_spike": len(
                [
                    log
                    for log in parsed_logs
                    if datetime.fromisoformat(log["timestamp"].replace("Z", ""))
                    > datetime.utcnow() - timedelta(minutes=30)
                ]
            )
            > len(parsed_logs) * 0.5
        },
    }

    return summary
