from google.cloud import vision


def image_summary(payload, config=None):
    client = vision.ImageAnnotatorClient()
    response = client.label_detection(image=vision.Image(content=payload["image_bytes"]), max_results=3)
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"summary": ", ".join(label.description for label in response.label_annotations[:3])}
