import boto3
import os
from typing import Dict, Any, List
import json
import tempfile
import zipfile


def export_documents_to_archive(
    documents: List[Dict[str, Any]], bucket_name: str, archive_key: str
) -> str:
    """
    Archives exported document snapshots in Amazon S3.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, "w") as zipf:
            for idx, doc in enumerate(documents):
                doc_json = json.dumps(doc, ensure_ascii=False, indent=2)
                zipf.writestr(f"document_{idx}.json", doc_json)

        # Upload to S3
        s3_client.upload_file(
            Filename=tmp_file.name, Bucket=bucket_name, Key=archive_key
        )

    return f"s3://{bucket_name}/{archive_key}"
