import boto3
from vision_client import get_rekognition_client
from vision_models import ImagePayload

def detect_image_text(payload: ImagePayload, config=None):
    config = config or {}
    client = get_rekognition_client(region_name=config.get("region"))
    response = client.detect_text(
        Image={"Bytes": payload.image_bytes}
    )

    detected_text = [
        text["DetectedText"]
        for text in response["TextDetections"]
        if text["Type"] == "WORD"
    ]
    return {"text": detected_text}
