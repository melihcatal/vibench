from collections import Counter
from typing import Iterable, Mapping

from google.cloud import bigquery


def summarize_messages(records: Iterable[Mapping[str, object]]) -> dict:
    status_counts = Counter(str(record.get("status", "unknown")) for record in records)
    return {"status_counts": dict(status_counts), "provider": "google-bigquery"}


def load_summary_from_bigquery(table_id: str) -> dict:
    client = bigquery.Client()
    rows = client.list_rows(table_id)
    return summarize_messages(rows)
