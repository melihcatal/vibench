from google.cloud import vision
from vision_client import get_vision_client


def detect_image_text(payload, config=None):
    config = config or {}
    client = get_vision_client()
    response = client.text_detection(
        image=vision.Image(content=payload["image_bytes"])
    )
    if response.error.message:
        raise RuntimeError(response.error.message)

    full_text = response.full_text_annotation.text if response.full_text_annotation else ""
    return {"detected_text": full_text}
