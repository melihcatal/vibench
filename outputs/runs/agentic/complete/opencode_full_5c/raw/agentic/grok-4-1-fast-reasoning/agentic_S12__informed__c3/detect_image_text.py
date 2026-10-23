import os
import boto3
from vision_client import load_image_bytes
from vision_models import ImageText

rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)


def detect_image_text(image_path: str) -> ImageText:
    image_bytes = load_image_bytes(image_path)
    response = rekognition.detect_text(Image={"Bytes": image_bytes})
    texts = [
        detection["DetectedText"]["Text"]
        for detection in response["TextDetections"]
        if detection["Type"] == "LINE" and detection["Confidence"] > 70.0
    ]
    return {"texts": texts}
