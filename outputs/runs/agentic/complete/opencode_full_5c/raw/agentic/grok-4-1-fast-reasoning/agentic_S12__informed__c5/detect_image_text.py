from vision_client import load_image_bytes, get_rekognition_client
from vision_models import parse_rekognition_text


def detect_image_text(image_path: str) -> dict:
    image_bytes = load_image_bytes(image_path)
    client = get_rekognition_client()
    response = client.detect_text(Image={"Bytes": image_bytes})
    return parse_rekognition_text(response)
