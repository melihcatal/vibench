import os
import boto3
from typing import List, Dict


def detect_image_text(image_path: str) -> List[Dict]:
    """Detect text appearing inside an image using AWS Rekognition."""
    rekognition_client = boto3.client(
        "rekognition",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = rekognition_client.detect_text(Image={"Bytes": image_bytes})

    text_detections = response.get("TextDetections", [])

    results = []
    for detection in text_detections:
        if detection["Type"] == "LINE":
            results.append(
                {
                    "text": detection["DetectedText"],
                    "confidence": detection["Confidence"],
                    "bounding_box": detection.get("Geometry", {}).get(
                        "BoundingBox", {}
                    ),
                }
            )

    return results
