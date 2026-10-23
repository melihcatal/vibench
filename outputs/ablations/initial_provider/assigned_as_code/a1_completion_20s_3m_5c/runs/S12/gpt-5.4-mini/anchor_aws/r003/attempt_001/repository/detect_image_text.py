import boto3

from vision_models import normalize_text_response


def detect_image_text(payload, config=None):
    config = config or {}
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_text(Image={"Bytes": payload["image_bytes"]}, MaxLabels=int(config.get("max_text_detections", 10)))
    lines = []
    text_parts = []
    for item in response.get("TextDetections", []):
        if item.get("Type") == "LINE":
            lines.append({"text": item.get("DetectedText", ""), "confidence": item.get("Confidence", 0.0) / 100.0})
            text_parts.append(item.get("DetectedText", ""))
    return normalize_text_response({"text": "\n".join(text_parts), "lines": lines})
