from datetime import datetime, timedelta, timezone

from observability_client import query_logs


def main() -> dict:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=12)
    query = "AzureDiagnostics | where SeverityLevel in ('Error', 'Critical') | summarize count() by ServiceName, bin(TimeGenerated, 1h)"
    result = query_logs(query, start_time=start, end_time=end)
    return {"findings": result.items}


if __name__ == "__main__":
    main()
