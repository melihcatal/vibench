import os
import boto3
from typing import List
from vision_models import ImageAnalysisRequest, ImageSafetyResult


def score_image_safety(request: ImageAnalysisRequest) -> List[ImageSafetyResult]:
    client = boto3.client(
        "rekognition",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get(
            "AWS_REGION", "us-east-1"
        ),  # Specify a default region if not set
    )

    if request.image_bytes:
        response = client.detect_moderation_labels(Image={"Bytes": request.image_bytes})
    elif request.image_url:
        # Rekognition expects S3 object or bytes, not direct URL for moderation
        # This is a simplification; a real implementation would download the image or use S3
        raise ValueError(
            "Amazon Rekognition requires image_bytes or an S3 object. image_url is not supported directly for moderation."
        )
    else:
        raise ValueError("Either image_url or image_bytes must be provided.")

    safety_results = []
    for label in response.get("ModerationLabels", []):
        safety_results.append(
            ImageSafetyResult(
                category=label["Name"],
                severity=int(
                    label["Confidence"]
                ),  # Confidence can be used as a proxy for severity
            )
        )
    return safety_results
