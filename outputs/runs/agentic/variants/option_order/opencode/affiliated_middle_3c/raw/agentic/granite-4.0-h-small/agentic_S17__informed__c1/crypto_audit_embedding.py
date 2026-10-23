import os
from google.cloud import bigquery
import json
from security_models import EncryptRequest

# Embedding crypto audit notes into a semantic search table
# For demonstration we upload a JSON record to BigQuery


def embed_audit_note(encrypt_req: EncryptRequest, note: str):
    """Upload an audit record associating crypto request with a note."""
    client = bigquery.Client()
    dataset_id = "crypto_audit"
    table_id = "notes"
    schema = [
        bigquery.SchemaField("request_id", "STRING"),
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("encrypt_request", "STRING"),
        bigquery.SchemaField("note", "STRING"),
    ]
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        schema=schema, skip_leading_rows=1, write_disposition="WRITE_APPEND"
    )
    rows = [
        {
            "request_id": encrypt_req.get("key_name", "N/A"),
            "timestamp": os.getenv("UPLOAD_TS", "2024-01-01 00:00:00 UTC"),
            "encrypt_request": json.dumps(encrypt_req),
            "note": note,
        }
    ]
    load_job = client.load_table_from_json(rows, table_ref, job_config=job_config)
    load_job.result()  # wait for completion
    print(f"Audit note embedded for request {encrypt_req.get('key_name')}")


if __name__ == "__main__":
    audit_note = "Key created for user data protection"
    req = {"key_name": os.getenv("KMS_KEY_ID", "example-key")}
    embed_audit_note(req, audit_note)
