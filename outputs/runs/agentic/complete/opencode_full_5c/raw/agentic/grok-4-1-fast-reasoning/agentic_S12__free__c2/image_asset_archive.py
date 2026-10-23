import os
import json
from google.cloud import storage


def image_asset_archive(
    image_path: str, analysis: dict, bucket_name: str = None
) -> str:
    if bucket_name is None:
        bucket_name = os.getenv("GCS_BUCKET_NAME")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    image_blob = bucket.blob(f"archives/{os.path.basename(image_path)}")
    image_blob.upload_from_filename(image_path)
    analysis_blob = bucket.blob(f"archives/{base_name}_analysis.json")
    analysis_blob.upload_from_string(json.dumps(analysis, indent=2))
    return f"gs://{bucket_name}/archives/{base_name}_analysis.json"
