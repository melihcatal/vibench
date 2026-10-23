import os
import base64
from typing import List
from vision_client import get_aws_rekognition_client
from vision_models import ImageInput, TextDetectionResult

def detect_image_text(image_input: ImageInput) -> List[TextDetectionResult]:
    client = get_aws_rekognition_client()

    image_payload = {}
    if image_input.image_bytes:
        image_payload["Bytes"] = image_input.image_bytes
    elif image_input.image_url:
        raise ValueError("AWS Rekognition DetectText API primarily uses image bytes or S3 objects. image_url not directly supported for this API call without intermediate S3 upload.")
    else:
        raise ValueError("ImageInput must contain image_bytes.")

    response = client.detect_text(Image=image_payload)

    detected_texts = []
    for text_detection in response["TextDetections"]:
        if text_detection["Type"] == "LINE":
            detected_texts.append(
                TextDetectionResult(
                    text=text_detection["DetectedText"],
                    bounding_box=text_detection["Geometry"]["BoundingBox"]
                )
            )
    return detected_texts