import boto3


def detect_image_text(payload, config=None):
    config = config or {}
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_text(
        Image={"Bytes": payload["image_bytes"]},
    )
    return {"text": [text_detection["DetectedText"] for text_detection in response["TextDetections"]]}