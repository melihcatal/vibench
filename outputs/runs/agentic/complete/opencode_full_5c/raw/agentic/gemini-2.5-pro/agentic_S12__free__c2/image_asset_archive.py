from google.cloud import storage
from vision_models import ArchiveResult
import os
import json
from typing import Dict, Any


def archive_analysis_artifacts(
    bucket_name: str, blob_name: str, analysis_data: Dict[str, Any]
) -> ArchiveResult:
    """Archives image analysis artifacts to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Convert the analysis data to a JSON string for uploading
    data_str = json.dumps(analysis_data, indent=2)

    blob.upload_from_string(data_str, content_type="application/json")

    # Reload the blob to get the generation number
    blob.reload()

    return ArchiveResult(
        bucket=bucket.name, blob_name=blob.name, generation=blob.generation
    )
