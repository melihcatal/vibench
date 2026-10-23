import json
import os
import boto3
from database_client import parse_response

# Provider: Amazon S3 (managed object storage) using boto3 SDK
# Assumes AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set (or using IAM role)
client = boto3.client('s3')

# Bucket name – could be parameterised; here we read from env
BUCKET_NAME = get_env_or_raise("S3_EXPORT_BUCKET")

model_id = "s3-export-archive"  # concrete provider identifier

def export_document_snapshot(raw_documents: dict, snapshot_id: str) -> None:
    """Archive a document snapshot or attachment to Amazon S3.
    Saves a JSON representation of the document as an object under the provided snapshot_id.
    Args:
        raw_documents: dict from parse_response (expects a single document under 'document').
        snapshot_id: Unique name for the archived object (e.g., UUID or timestamp).
    """
    document = raw_documents.get('document')
    if not document:
        raise ValueError("No document found in response to export")

    # Serialize document to JSON string
    payload = json.dumps(document, indent=2).encode('utf-8')

    try:
        client.put_object(
            Bucket=BUCKET_NAME,
            Key=snapshot_id + ".json",
            Body=payload
        )
    except Exception as e:
        raise RuntimeError(f"Failed to upload to S3: {str(e)}")

# Helper that throws if required env var missing
get_env_or_raise = lambda var: \\\n    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
