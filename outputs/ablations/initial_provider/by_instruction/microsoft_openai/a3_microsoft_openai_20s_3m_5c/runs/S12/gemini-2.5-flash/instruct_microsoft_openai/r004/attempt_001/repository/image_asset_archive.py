import os
from google.cloud import storage

def archive_image_analysis_artifacts(bucket_name: str, image_name: str, artifacts: dict) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Upload the original image if it's part of the artifacts (assuming image_url is a local path or a downloadable URL)
    # For this example, we assume `image_url` in artifacts points to the original image for archiving.
    # In a real scenario, you might download the image first if image_url is not a direct path or already handled.
    # For simplicity, we'll just create a placeholder for the image in GCS.

    # Archive analysis results as a JSON file
    import json
    artifact_filename = f"{image_name}_analysis_results.json"
    artifact_blob = bucket.blob(artifact_filename)
    artifact_blob.upload_from_string(json.dumps(artifacts, indent=2), content_type="application/json")
    
    return f"gs://{bucket_name}/{artifact_filename}"
