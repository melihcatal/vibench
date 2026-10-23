import os
from typing import List, Dict, Any
from vision_client import get_vision_client


def detect_image_text(image_path: str) -> List[Dict[str, Any]]:
    """
    Detect text appearing inside an image using Amazon Rekognition.

    Args:
        image_path: Path to the image file

    Returns:
        List of text detection dictionaries with 'text' and 'confidence' keys
    """
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={"Bytes": image_bytes})

    text_detections = []
    for detection in response["TextDetections"]:
        if detection["Type"] == "LINE":
            text_detections.append(
                {
                    "text": detection["DetectedText"],
                    "confidence": detection["Confidence"],
                    "type": detection["Type"],
                }
            )

    return text_detections
