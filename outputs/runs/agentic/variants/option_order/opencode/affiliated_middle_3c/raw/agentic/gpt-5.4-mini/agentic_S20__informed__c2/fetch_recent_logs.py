from datetime import datetime, timedelta, timezone

from observability_client import create_client


def fetch_recent_logs() -> dict:
    client = create_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    params = {
        "from": start.isoformat().replace("+00:00", "Z"),
        "to": end.isoformat().replace("+00:00", "Z"),
        "query": "service:api status:200",
    }
    response = client.get("/api/v2/logs/events", params=params)
    return {"status_code": response.status_code, "body": response.text}
