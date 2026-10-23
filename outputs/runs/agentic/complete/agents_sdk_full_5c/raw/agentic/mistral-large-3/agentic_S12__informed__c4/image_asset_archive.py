import os
from typing import Dict, Optional
from ibm_botocore.client import Config
import ibm_boto3
from vision_models import (
    LabelDetectionResponse,
    ImageDescriptionResponse,
    TextDetectionResponse,
    ImageSafetyResponse
)


def archive_image_analysis_artifacts(
    image_path: str,
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse,
    text: TextDetectionResponse,
    safety: ImageSafetyResponse,
    bucket_name: str = "image-analysis-archive"
) -> str:
    """Archives image analysis artifacts in IBM Cloud Object Storage."""
    cos_endpoint = os.getenv("IBM_COS_ENDPOINT")
    cos_apikey = os.getenv("IBM_COS_APIKEY")
    cos_client = ibm_boto3.client(
        "s3",
        endpoint_url=cos_endpoint,
        aws_access_key_id="cos_apikey",
        aws_secret_access_key=cos_apikey,
        config=Config(signature_version="oauth")
    )

    object_key = f"analysis_{os.path.basename(image_path)}.json"
    metadata = {
        "labels": labels.dict(),
        "description": description.dict(),
        "text": text.dict(),
        "safety": safety.dict()
    }

    cos_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=str(metadata).encode("utf-8")
    )

    return f"cos://{bucket_name}/{object_key}"