import os
import json
from google.cloud import storage


def archive_analysis_assets(
    image_path: str, analysis_output: dict, safe_labels: list, description: str
):
    """Archive all intermediate artifacts (labels, description, safety check) into a JSON file stored in managed object storage.

    Args:
        image_path: Original image file path.
        analysis_output: Dict of step names to their responses (as returned by each step).
        safe_labels: List of safe label strings after filtering.
        description: Generated description string.

    Returns:
        URI of the archived JSON blob.
    """
    # Build a tidy archive payload
    archive_payload = {
        "image_path": image_path,
        "analysis_timestamp": os.getenv(
            "ARCHIVE_TIMESTAMP", json.dumps({"now": json.dumps({"now": ""})})
        ),
        # Store raw responses per step (normalized later)
        "analysis_output": analysis_output,
        "safe_labels": safe_labels,
        "description": description,
    }
    # Prepare storage location (using env variable for bucket name)
    bucket_name = os.getenv("ASSET_ARCHIVE_BUCKET", "my-archive-bucket")
    blob_name = f"archive/{os.path.splitext(os.path.basename(image_path))[0]}.json"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(
        json.dumps(archive_payload, indent=2), content_type="application/json"
    )
    return f"gs://{bucket_name}/{blob_name}"
