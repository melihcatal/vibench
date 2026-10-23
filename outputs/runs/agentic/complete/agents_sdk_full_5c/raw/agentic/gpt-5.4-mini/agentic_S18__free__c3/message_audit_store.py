import os
from typing import Iterable

from google.cloud import bigquery

from messaging_models import MessageRecord


# Persists Pub/Sub processing audits into Google BigQuery.
def store_audit_records(records: Iterable[MessageRecord]) -> int:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    table_id = os.environ.get("AUDIT_TABLE", f"{project_id}.messaging_audit.processed_messages")
    client = bigquery.Client(project=project_id)
    rows = [
        {
            "message_id": record.message_id,
            "status": record.status,
            "body": record.body,
            "attributes": record.attributes,
            "processed_at": record.processed_at,
        }
        for record in records
    ]
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        raise RuntimeError(str(errors))
    return len(rows)
