import json
from vision_client import VisionClient  # Amazon Rekognition


def detect_image_text(image_path: str) -> list:
    """Detects text that appears within an image using Amazon Rekognition.

    Returns a list of detected text strings.
    """
    client = VisionClient()  # Rekognition client via boto3
    response = client.detect_text(Image={"Bytes": client.read_image(image_path)})
    texts = [text["DetectedText"] for text in response.get("TextDetections", [])]
    return texts
