from datetime import datetime, timedelta, timezone

from observability_client import create_client


def query_error_logs() -> dict:
    client = create_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=1)
    query = {
        "filter": {
            "from": start.isoformat().replace("+00:00", "Z"),
            "to": end.isoformat().replace("+00:00", "Z"),
            "query": "severity:error OR severity:ERROR",
        }
    }
    response = client.post("/api/v2/logs/events/search", query)
    return {"status_code": response.status_code, "body": response.text}
