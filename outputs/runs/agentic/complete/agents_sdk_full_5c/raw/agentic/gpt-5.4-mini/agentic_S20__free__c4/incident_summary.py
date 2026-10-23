from __future__ import annotations

from collections import Counter

from observability_client import build_client


def main() -> dict:
    client = build_client()
    result = client.query_errors(severity="ERROR", minutes=240, limit=50)
    counts = Counter(record.message for record in result.records)
    top = counts.most_common(5)
    return {"provider": "google-cloud-logging", "filter": result.filter_expression, "top_errors": top}
