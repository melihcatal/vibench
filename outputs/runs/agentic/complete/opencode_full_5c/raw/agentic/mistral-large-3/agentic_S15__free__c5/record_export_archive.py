from typing import Dict, List, IO
import boto3
import tempfile
import json
import os


def record_export_archive(
    documents: List[Dict[str, Any]], bucket_name: str
) -> Dict[str, str]:
    """Archive exported document snapshots in AWS S3 managed object storage."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as tmp_file:
        json.dump(documents, tmp_file)
        tmp_file_path = tmp_file.name

    archive_key = f"document_archives/{os.path.basename(tmp_file_path)}"
    s3_client.upload_file(tmp_file_path, bucket_name, archive_key)
    os.unlink(tmp_file_path)

    return {"bucket": bucket_name, "key": archive_key, "status": "archived"}
