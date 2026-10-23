import os
import boto3
import json
from typing import Dict, Any


def image_asset_archive(
    image_path: str,
    analyses: Dict[str, Any],
    bucket_name: str,
    prefix: str = "vision-analysis",
) -> Dict[str, str]:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    image_filename = os.path.basename(image_path)
    image_key = f"{prefix}/{image_filename}"
    s3_client.upload_file(image_path, bucket_name, image_key)

    analyses_key = f"{prefix}/{os.path.splitext(image_filename)[0]}_analysis.json"
    analyses_json = json.dumps(analyses, indent=2).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=analyses_key,
        Body=analyses_json,
        ContentType="application/json",
    )

    return {"bucket": bucket_name, "image_key": image_key, "analyses_key": analyses_key}
