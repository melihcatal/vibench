from google.cloud import storage
import os

def image_asset_archive(payload, config=None):
    config = config or {}
    client = storage.Client()

    bucket_name = config.get("bucket_name", os.environ.get("GCS_BUCKET_NAME"))
    if not bucket_name:
        raise ValueError("Google Cloud Storage bucket name not provided.")

    bucket = client.bucket(bucket_name)

    image_bytes = payload.get("image_bytes")
    image_filename = payload.get("image_filename", "archive_image.jpg")
    analysis_artifacts = payload.get("analysis_artifacts", {})
    captions = payload.get("captions", {})

    # Upload image bytes if provided
    if image_bytes:
        image_blob = bucket.blob(f"images/{image_filename}")
        image_blob.upload_from_string(image_bytes, content_type=payload.get("image_mime_type", "image/jpeg"))
        image_url = image_blob.public_url
    else:
        image_url = None

    # Upload analysis artifacts (e.g., JSON of labels, text, safety scores)
    if analysis_artifacts:
        artifact_filename = f"artifacts/{os.path.splitext(image_filename)[0]}_analysis.json"
        artifact_blob = bucket.blob(artifact_filename)
        import json
        artifact_blob.upload_from_string(json.dumps(analysis_artifacts), content_type="application/json")
        artifact_url = artifact_blob.public_url
    else:
        artifact_url = None

    # Upload captions
    if captions:
        caption_filename = f"captions/{os.path.splitext(image_filename)[0]}_captions.json"
        caption_blob = bucket.blob(caption_filename)
        import json
        caption_blob.upload_from_string(json.dumps(captions), content_type="application/json")
        caption_url = caption_blob.public_url
    else:
        caption_url = None

    return {
        "image_archive_url": image_url,
        "artifacts_archive_url": artifact_url,
        "captions_archive_url": caption_url
    }
