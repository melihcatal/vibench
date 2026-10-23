import os
from typing import Dict, List
import boto3
from botocore.exceptions import ClientError
from .vision_models import (
    LabelDetectionResponse,
    ImageDescriptionResponse,
    TextDetectionResponse,
    SafetyScoreResponse,
)


def image_asset_archive(
    image_path: str,
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse,
    texts: TextDetectionResponse,
    safety_score: SafetyScoreResponse,
    bucket_name: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
) -> str:
    """
    Archives image-analysis artifacts and derived captions in Amazon S3.
    """
    aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket_name = bucket_name or os.getenv("AWS_S3_BUCKET_NAME")

    if not aws_access_key_id or not aws_secret_access_key or not bucket_name:
        raise ValueError(
            "AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_S3_BUCKET_NAME must be set."
        )

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Prepare metadata
    metadata = {
        "labels": ",".join(labels.labels),
        "description": description.description,
        "texts": ",".join(texts.texts) if texts.texts else "None",
        "safety_score": str(safety_score.score),
        "safety_reason": safety_score.reason,
    }

    # Upload image
    image_key = f"images/{os.path.basename(image_path)}"
    s3_client.upload_file(image_path, bucket_name, image_key)

    # Upload metadata
    metadata_key = f"metadata/{os.path.basename(image_path)}.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=metadata_key,
        Body=str(metadata),
        ContentType="application/json",
    )

    return f"s3://{bucket_name}/{metadata_key}"
