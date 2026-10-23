import os
import json
import boto3
from database_client import fetch_document
from record_text_safety import check_text_safety

# ------------------------------------------------------------
# record_export_archive.py
# ------------------------------------------------------------
# Uses Amazon S3 as the managed object storage provider

# AWS credentials are expected to be available in the environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
S3_CLIENT = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET', 'my-export-bucket')

# Example: export a processed document snapshot to S3 (private object)
def archive_snapshot(document: dict, key: str):
    # Ensure document is JSON-serializable
    payload = json.dumps(document, indent=2).encode('utf-8')
    # Optional: apply safety check before storing (example only)
    # safe_description = check_text_safety(document.get('description',''))
    # document['description'] = safe_description
    S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=key, Body=payload, ACL='private')

    print(f"Archived {key} to S3 bucket {S3_BUCKET}")

# Demonstration
if __name__ == "__main__":
    doc_id = 'user-123'
    doc = fetch_document('mydb', doc_id)
    if doc:
        archive_snapshot(doc, f"snapshots/{doc_id}.json")
    else:
        print(f"Document {doc_id} not found")
