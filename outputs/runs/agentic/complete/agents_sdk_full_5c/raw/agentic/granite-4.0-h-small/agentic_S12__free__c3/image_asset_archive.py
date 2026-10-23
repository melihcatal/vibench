import os
import json
import uuid
from google.cloud import storage

def archive_image_analysis(image_path, analyses):
    """Archive image, analysis metadata, labels, text, and captions into Cloud Storage under a unique folder.
    analyses: dict of analysis_name -> result list/dict (e.g., labels, extracted_text)
    Returns the generated bucket name and blob path prefix.
    """
    client = storage.Client()
    bucket_name = f"vision-analysis-{uuid.uuid4().hex[:8]}"
    bucket = client.create_bucket(bucket_name)
    blob_prefix = f"assets/{uuid.uuid4().hex[:12]}/"
    # 1. Upload original image
    image_blob = f"{blob_prefix}original_image.jpg"
    bucket.blob(image_blob).upload_from_filename(image_path)
    # 2. Store metadata JSON
    meta = {
        "image_path": image_path,
        "analyses": analyses,
        "uploaded_at": os.getenv("NOW", "1970-01-01T00:00:00Z"),
    }
    meta_blob = f"{blob_prefix}analysis_metadata.json"
    bucket.blob(meta_blob).upload_from_string(json.dumps(meta))
    # 3. (Optional) upload each extracted text as separate blob if needed
    return {
        "bucket": bucket_name,
        "prefix": blob_prefix,
    }
