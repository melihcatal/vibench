from google.cloud import vision
from vision_client import get_vision_client


def image_summary(image_path):
    client = get_vision_client()
    labels = detect_image_labels(image_path)
    description = describe_image(image_path)
    texts = detect_image_text(image_path)
    safety = score_image_safety(image_path)
    return {
        "labels": labels,
        "description": description,
        "texts": texts,
        "safety": safety,
    }
