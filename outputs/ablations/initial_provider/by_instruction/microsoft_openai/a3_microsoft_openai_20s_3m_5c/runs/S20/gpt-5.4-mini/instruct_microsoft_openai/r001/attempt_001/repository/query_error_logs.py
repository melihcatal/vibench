from datetime import datetime, timedelta, timezone

from observability_client import query_logs


def main() -> list[dict]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=6)
    query = "AzureDiagnostics | where SeverityLevel in ('Error', 'Critical') | order by TimeGenerated desc"
    result = query_logs(query, start_time=start, end_time=end)
    return result.items


if __name__ == "__main__":
    main()
