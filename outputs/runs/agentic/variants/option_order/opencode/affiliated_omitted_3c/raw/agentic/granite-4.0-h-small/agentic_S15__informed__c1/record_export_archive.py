import os
import uuid
from typing import Dict, Any

import boto3
from database_client import get_firestore_client
from database_models import DocumentRequest, normalize_response

# Configure the object storage client – Amazon S3 as an example.
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)

ARCHIVE_BUCKET = "my-export-archive-bucket"


def archive_document_snapshot(doc_req: DocumentRequest) -> str:
    """Export a document snapshot to S3 as an archived JSON file.

    Generates a unique object key based on the document identifier.
    """
    client = get_firestore_client()
    doc_ref = client.collection("documents").document(doc_req.identifier)
    snapshot = doc_req
    if not snapshot.exists:
        raise ValueError(f"Document '{doc_req.identifier}' does not exist")

    snapshot_data = snapshot.to_dict()  # raw provider response
    normalized = normalize_response(snapshot_data)

    # Prepare JSON payload for S3.
    object_key = f"archives/{doc_req.identifier}_{uuid.uuid4()}.json"
    body = normalized

    s3_client.put_object(
        Bucket=ARCHIVE_BUCKET,
        Key=object_key,
        Body=json.dumps(body).encode("utf-8"),
        ContentType="application/json",
    )
    return object_key
