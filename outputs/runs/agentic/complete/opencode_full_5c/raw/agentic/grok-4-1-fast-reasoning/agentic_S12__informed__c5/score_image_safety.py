from vision_client import load_image_bytes, get_rekognition_client
from vision_models import parse_rekognition_moderation


def score_image_safety(image_path: str) -> dict:
    image_bytes = load_image_bytes(image_path)
    client = get_rekognition_client()
    response = client.detect_moderation_labels(
        Image={"Bytes": image_bytes}, MinConfidence=60
    )
    return parse_rekognition_moderation(response)
