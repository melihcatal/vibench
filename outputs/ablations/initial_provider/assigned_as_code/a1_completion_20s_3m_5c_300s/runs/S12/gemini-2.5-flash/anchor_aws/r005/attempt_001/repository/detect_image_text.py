from vision_client import get_rekognition_client
from vision_models import normalize_text_detections


def detect_image_text(payload, config=None):
    config = config or {}
    client = get_rekognition_client(region_name=config.get("region"))
    response = client.detect_text(
        Image={"Bytes": payload["image_bytes"]}
    )
    return {"text_detections": normalize_text_detections(response)}
