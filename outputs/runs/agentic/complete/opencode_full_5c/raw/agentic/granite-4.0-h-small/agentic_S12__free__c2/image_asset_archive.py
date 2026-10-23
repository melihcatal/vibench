import os
import json
import boto3
from typing import List, Dict, Any
from vision_models import VisionResponse

# Archive visual analysis artifacts and derived captions in managed object storage (S3)


def archive_image_assets(image_path: str, analysis: VisionResponse) -> str:
    """Package analysis results and upload to an S3 bucket for long‑term storage.","""
    # Provider specific: AWS S3 via boto3 (any other managed storage would work)
    bucket_name = os.getenv("IMAGE_ARCHIVE_BUCKET")
    if not bucket_name:
        raise RuntimeError("IMAGE_ARCHIVE_BUCKET not configured")
    s3_client = boto3.client("s3")

    # Serialize results
    payload = {
        "image_path": image_path,
        "labels": analysis.get("labels", []),
        "description": analysis.get("description", ""),
        "extracted_text": analysis.get("text", []),
        "safe": analysis.get("safe", False),
        "timestamp": int(os.time()),
    }
    object_key = f"analysis/{os.path.basename(image_path)}.json"
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=json.dumps(payload))
    return f"s3://{bucket_name}/{object_key}"


# Export for downstream workflows
__all__ = ["archive_image_assets"]
