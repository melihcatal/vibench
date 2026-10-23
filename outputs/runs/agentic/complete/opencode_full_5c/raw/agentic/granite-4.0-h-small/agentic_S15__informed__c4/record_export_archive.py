import json
import os
from typing import Dict, Any
from database_models import DocumentResponse, ArchiveEntry
from database_client import client


def archive_snapshot(
    doc: DocumentResponse, destination_bucket: str = "snapshots"
) -> None:
    """
    Stores a snapshot (full document payload and metadata) in the configured object storage.
    Uses env variables to select the concrete storage provider.
    """
    environment = get_storage_env()
    bucket = environment.get("BUCKET", destination_bucket)
    region = environment.get("REGION", "us-east-1")
    # Choose storage client based on env variable (placeholder logic)
    if environment["service"] == "s3":
        return upload_to_s3(doc, bucket, region)
    elif environment["service"] == "gcs":
        return upload_to_gcs(doc, bucket)
    elif environment["service"] == "cos":
        return upload_to_cos(doc, bucket)
    else:
        raise NotImplementedError(
            f"Unsupported object storage service: {environment['service']}"
        )


# Helper: SCANNING environment variable configuration
def get_storage_env() -> Dict[str, Any]:
    return {
        "service": os.getenv(
            "OBJ_STORAGE_SERVICE", "s3"
        ),  # s3 / gcs / cos / azure / b2 / aliyun
        "BUCKET": os.getenv("OBJ_STORAGE_BUCKET"),
        "REGION": os.getenv("OBJ_STORAGE_REGION"),
    }


# ---- Provider-specific upload functions (dummies) ----
def upload_to_s3(doc: DocumentResponse, bucket: str, region: str) -> None:
    # Example: Boto3 S3 client code omitted for brevity
    print(
        f"[ARCHIVE] Storing {doc.id} to S3://{bucket}/{doc.id}.json (region={region})"
    )


def upload_to_gcs(doc: DocumentResponse, bucket: str) -> None:
    print(f"[ARCHIVE] Storing {doc.id} to GCS://{bucket}/{doc.id}.json")


def upload_to_cos(doc: DocumentResponse, bucket: str) -> None:
    print(f"[ARCHIVE] Storing {doc.id} to IBM COS://{bucket}/{doc.id}.json")


# Example CLI – fetch a document, archive it
if __name__ == "__main__":
    sample_id = "demo-004"
    try:
        fetched = client.get_client().find_one(
            {"id": sample_id}
        )  # placeholder; call appropriate fetch
        # Build a DocumentResponse manually for archiving
        doc = DocumentResponse(id=sample_id, data=fetched, version=0)
        archive_snapshot(doc)
    except Exception as e:
        print(f"Failed to archive: {e}")
