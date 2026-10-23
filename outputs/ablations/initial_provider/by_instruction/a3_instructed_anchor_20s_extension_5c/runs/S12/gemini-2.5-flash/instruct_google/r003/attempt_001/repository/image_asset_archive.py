from google.cloud import storage
import os
import json

def archive_image_analysis_artifacts(image_path: str, analysis_results: dict, bucket_name: str) -> dict:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        return {"error": "GCP_PROJECT_ID environment variable not set for archiving.", "image_uri": None, "analysis_uri": None}

    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)

    # Upload the original image
    image_filename = os.path.basename(image_path)
    image_blob = bucket.blob(f"images/{image_filename}")
    image_blob.upload_from_filename(image_path)
    image_uri = f"gs://{bucket_name}/images/{image_filename}"

    # Store the analysis results as a JSON file
    analysis_filename = f"{os.path.splitext(image_filename)[0]}_analysis.json"
    analysis_blob = bucket.blob(f"analysis/{analysis_filename}")
    analysis_blob.upload_from_string(json.dumps(analysis_results), content_type="application/json")
    analysis_uri = f"gs://{bucket_name}/analysis/{analysis_filename}"

    return {"image_uri": image_uri, "analysis_uri": analysis_uri}
