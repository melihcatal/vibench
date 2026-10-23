from google.cloud import storage
import datetime

def archive_image_analysis_artifacts(
    image_bytes: bytes,
    image_filename: str,
    analysis_results: dict,
    bucket_name: str,
    project_id: str = None
):
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        image_bytes: The original image bytes.
        image_filename: The original filename of the image.
        analysis_results: A dictionary containing all analysis results (e.g., labels, description, text, safety).
        bucket_name: The name of the Google Cloud Storage bucket to archive to.
        project_id: The Google Cloud project ID. If not provided, it will be inferred from the environment.

    Returns:
        A dictionary with URLs of the archived image and its analysis results.
    """
    if not project_id:
        try:
            import google.auth
            credentials, project_id = google.auth.default()
        except Exception:
            raise ValueError("Google Cloud project ID must be provided or discoverable from the environment.")

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    # Generate a unique path for the archive
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    base_blob_path = f"image_archives/{timestamp}/{image_filename.split('.')[0]}"

    # Archive original image
    image_blob = bucket.blob(f"{base_blob_path}/{image_filename}")
    image_blob.upload_from_string(image_bytes, content_type='image/jpeg') # Assuming jpeg, adjust if needed

    # Archive analysis results as a JSON file
    import json
    analysis_json = json.dumps(analysis_results, indent=2)
    results_blob = bucket.blob(f"{base_blob_path}/analysis_results.json")
    results_blob.upload_from_string(analysis_json, content_type='application/json')

    return {
        "image_url": image_blob.public_url,
        "analysis_results_url": results_blob.public_url,
    }
