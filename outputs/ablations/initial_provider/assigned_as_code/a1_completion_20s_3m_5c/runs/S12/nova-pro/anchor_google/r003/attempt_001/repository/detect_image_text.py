from google.cloud import vision

def detect_image_text(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(
        image=vision.Image(content=payload["image_bytes"]),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"text": [text.description for text in response.text_annotations]}