from google.cloud import storage
import os
from typing import Dict, List
import json
import tempfile


def archive_image_analysis_artifacts(
    image_path: str,
    labels: List[Dict],
    description: str,
    texts: List[Dict],
    summary: str,
    bucket_name: str,
) -> str:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Create a temporary JSON file for analysis results
    analysis_data = {
        "labels": labels,
        "description": description,
        "texts": texts,
        "summary": summary,
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as temp_file:
        json.dump(analysis_data, temp_file)
        temp_file_path = temp_file.name

    # Upload the original image
    image_blob = bucket.blob(f"analysis/{os.path.basename(image_path)}")
    image_blob.upload_from_filename(image_path)

    # Upload the analysis results
    analysis_blob = bucket.blob(f"analysis/{os.path.basename(image_path)}.json")
    analysis_blob.upload_from_filename(temp_file_path)

    # Clean up
    os.unlink(temp_file_path)

    return f"gs://{bucket_name}/analysis/{os.path.basename(image_path)}"
