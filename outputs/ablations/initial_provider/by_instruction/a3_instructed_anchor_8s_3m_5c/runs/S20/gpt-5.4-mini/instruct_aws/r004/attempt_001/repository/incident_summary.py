from collections import Counter
from datetime import datetime, timedelta, timezone

import boto3

from observability_client import query_logs
from observability_models import QueryWindow


def summarize() -> dict:
    window = QueryWindow(start_time=datetime.now(timezone.utc) - timedelta(hours=6), end_time=datetime.now(timezone.utc), severity="ERROR")
    results = query_logs(window)
    counts = Counter()
    for row in results:
        for field in row:
            if field.get("field") == "service":
                counts[field.get("value", "unknown")] += 1
    return {"provider": "aws-cloudwatch-logs", "service_counts": dict(counts), "total": len(results)}


if __name__ == "__main__":
    summarize()
