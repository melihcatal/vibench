from google.cloud import vision

def describe_image(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(
        image=vision.Image(content=payload["image_bytes"]),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"description": response.text_annotations[0].description if response.text_annotations else "No text found"}