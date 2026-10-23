import boto3
from vision_client import image_to_bytes
from vision_models import VisionOCR


def detect_image_text(image_path: str) -> VisionOCR:
    rekognition = boto3.client("rekognition")
    image_bytes = image_to_bytes(image_path)
    response = rekognition.detect_text(Image={"Bytes": image_bytes})
    texts = [detection["DetectedText"] for detection in response["TextDetections"]]
    return VisionOCR(texts=texts)
