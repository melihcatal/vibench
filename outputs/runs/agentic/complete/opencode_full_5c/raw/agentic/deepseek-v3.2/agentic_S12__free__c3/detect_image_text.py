import os
from typing import List, Dict, Any
import boto3
from vision_client import get_aws_credentials


def detect_image_text(image_path: str) -> List[Dict[str, Any]]:
    """
    Detect text appearing inside an image using AWS Rekognition.

    Args:
        image_path: Path to the image file

    Returns:
        List of dictionaries containing detected text information
    """
    aws_access_key, aws_secret_key, region = get_aws_credentials()

    client = boto3.client(
        "rekognition",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region,
    )

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={"Bytes": image_bytes})

    result = []
    for text_detection in response["TextDetections"]:
        result.append(
            {
                "text": text_detection["DetectedText"],
                "confidence": text_detection["Confidence"],
                "type": text_detection["Type"],
                "geometry": {
                    "bounding_box": text_detection.get("Geometry", {}).get(
                        "BoundingBox", {}
                    ),
                    "polygon": text_detection.get("Geometry", {}).get("Polygon", []),
                },
            }
        )

    return result
