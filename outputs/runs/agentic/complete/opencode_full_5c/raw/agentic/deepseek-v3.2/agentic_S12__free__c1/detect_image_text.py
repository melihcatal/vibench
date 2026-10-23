import os
import boto3
from vision_client import get_aws_credentials


def detect_image_text(image_path: str):
    """Detects text appearing inside an image using Amazon Rekognition."""
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

    text_detections = response.get("TextDetections", [])

    result = []
    for detection in text_detections:
        if detection["Type"] == "LINE":
            result.append(
                {
                    "text": detection["DetectedText"],
                    "confidence": detection["Confidence"],
                    "geometry": {
                        "bounding_box": detection["Geometry"]["BoundingBox"],
                        "polygon": detection["Geometry"]["Polygon"],
                    },
                }
            )

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_image_text.py <image_path>")
        sys.exit(1)

    text_items = detect_image_text(sys.argv[1])
    for item in text_items:
        print(f"Text: {item['text']} (Confidence: {item['confidence']:.2f})")
