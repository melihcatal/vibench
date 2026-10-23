from vision_client import image_bytes, rekognition_client
from vision_models import normalize_text


def detect_image_text(source):
    client = rekognition_client()
    response = client.detect_text(Image={"Bytes": image_bytes(source)})
    return normalize_text(response.get("TextDetections"))
