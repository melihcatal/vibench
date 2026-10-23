from google.cloud import vision


def detect_image_text(payload, config=None):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(image=vision.Image(content=payload["image_bytes"]))
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"text": response.full_text_annotation.text if response.full_text_annotation else ""}
