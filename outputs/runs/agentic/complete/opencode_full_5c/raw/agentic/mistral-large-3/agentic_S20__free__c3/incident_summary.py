from typing import Dict, List
from observability_client import get_logging_client
from observability_models import LogQueryFilter


def summarize_incident_logs(filter: LogQueryFilter) -> Dict[str, Any]:
    """Summarize error-log findings from New Relic for incident review."""
    client = get_logging_client()

    # Build the NRQL query for New Relic Logs
    severity_conditions = " OR ".join(
        [f"level:'{severity.upper()}'" for severity in filter.severities]
    )
    query = (
        f"SELECT count(*) as count, level, message "
        f"FROM Log "
        f"WHERE {severity_conditions} "
        f"SINCE {filter.time_range_seconds} SECONDS AGO "
        f"FACET level, message "
        f"LIMIT {filter.limit}"
    )

    # Execute the query
    response = client.query(query)

    # Process the results
    summary = {"total_errors": 0, "severity_distribution": {}, "common_messages": []}

    for result in response.get("results", []):
        level = result.get("level", "UNKNOWN")
        message = result.get("message", "No message")
        count = result.get("count", 0)

        summary["total_errors"] += count
        summary["severity_distribution"][level] = (
            summary["severity_distribution"].get(level, 0) + count
        )
        summary["common_messages"].append({"message": message, "count": count})

    return summary
