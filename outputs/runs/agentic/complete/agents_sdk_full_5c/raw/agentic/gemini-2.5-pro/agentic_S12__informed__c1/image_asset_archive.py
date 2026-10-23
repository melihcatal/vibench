import os
import json
from dataclasses import asdict
import boto3
from vision_models import VisionResult


def archive_vision_result(
    vision_result: VisionResult, bucket_name: str, object_key: str
) -> dict:
    """
    Archives the vision analysis result as a JSON object in Amazon S3.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    result_dict = asdict(vision_result)
    result_json = json.dumps(result_dict, indent=2)

    try:
        s3_client.put_object(
            Bucket=bucket_name, Key=object_key, Body=result_json, ContentType="application/json"
        )
        return {"status": "success", "bucket": bucket_name, "key": object_key}
    except Exception as e:
        return {"status": "error", "message": str(e)}
