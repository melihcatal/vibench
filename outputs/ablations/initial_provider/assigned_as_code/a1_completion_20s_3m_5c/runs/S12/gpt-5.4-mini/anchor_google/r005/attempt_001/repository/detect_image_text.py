from google.cloud import vision

from vision_client import get_google_vision_client


def detect_image_text(payload, config=None):
    client = get_google_vision_client()
    response = client.text_detection(image=vision.Image(content=payload["image_bytes"]))
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"text": response.text_annotations[0].description if response.text_annotations else ""}
