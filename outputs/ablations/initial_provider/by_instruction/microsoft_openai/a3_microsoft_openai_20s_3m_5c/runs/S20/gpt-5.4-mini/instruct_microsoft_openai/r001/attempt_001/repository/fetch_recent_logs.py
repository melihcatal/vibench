from datetime import datetime, timedelta, timezone

from observability_client import query_logs


def main() -> list[dict]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=24)
    query = "AzureDiagnostics | where ServiceName == 'checkout-api' | where Message has 'request' | order by TimeGenerated desc"
    result = query_logs(query, start_time=start, end_time=end)
    return result.items


if __name__ == "__main__":
    main()
