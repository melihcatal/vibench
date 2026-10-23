from gcs_client import GCSClient
import json
from typing import Dict, Any, Optional


def image_asset_archive(
    bucket_name: str,
    file_name: str,
    artifact_data: Dict[str, Any],
    image_content: Optional[bytes] = None,
):
    client = GCSClient().get_client()
    bucket = client.bucket(bucket_name)

    # Upload artifact data as a JSON file
    artifact_blob = bucket.blob(f"{file_name}.json")
    artifact_blob.upload_from_string(
        json.dumps(artifact_data, indent=2), content_type="application/json"
    )

    # Upload original image content if provided
    if image_content:
        image_blob = bucket.blob(file_name)
        image_blob.upload_from_string(
            image_content, content_type="image/jpeg"
        )  # Assuming JPEG, could be dynamic

    print(f"Archived {file_name}.json and optional image to gs://{bucket_name}")
