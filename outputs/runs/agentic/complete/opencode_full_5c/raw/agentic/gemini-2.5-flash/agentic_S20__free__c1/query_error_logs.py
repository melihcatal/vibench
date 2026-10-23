import os
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import LogQueryResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def query_error_logs(
    severity: str = "ERROR", time_range_minutes: int = 60
) -> list[LogQueryResult]:
    client = ObservabilityClient(project_id=PROJECT_ID)

    now = datetime.utcnow()
    time_ago = now - timedelta(minutes=time_range_minutes)

    # Google Cloud Logging filter syntax
    filter_str = (
        f"severity>={severity.upper()} AND "
        f'timestamp>="{time_ago.isoformat("T")[:-3]}Z" AND '
        f'timestamp<="{now.isoformat("T")[:-3]}Z"'
    )

    print(
        f"Querying Google Cloud Logging for logs with severity>={severity.upper()} in the last {time_range_minutes} minutes..."
    )
    results = client.query_logs(filter_str=filter_str)

    if results:
        print(f"Found {len(results)} error logs:")
        for res in results:
            print(
                f"  [{res.timestamp}] [{res.severity}] {res.message} (Resource: {res.resource_type})"
            )
    else:
        print("No error logs found matching the criteria.")
    return results


if __name__ == "__main__":
    # Example usage:
    error_logs = query_error_logs(severity="ERROR", time_range_minutes=30)
