from typing import Dict, List, Any, Optional
import os
from google.cloud import storage
import json
import tempfile


def record_export_archive(
    documents: List[Dict[str, Any]], bucket_name: Optional[str] = None
) -> str:
    if not bucket_name:
        bucket_name = os.getenv(
            "GOOGLE_CLOUD_STORAGE_BUCKET", "document-archive-bucket"
        )

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as temp_file:
        json.dump(documents, temp_file)
        temp_file_path = temp_file.name

    blob = bucket.blob(f"archive_{os.path.basename(temp_file_path)}")
    blob.upload_from_filename(temp_file_path)

    os.unlink(temp_file_path)
    return f"gs://{bucket_name}/{blob.name}"
