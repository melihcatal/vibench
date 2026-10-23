from google.cloud import vision
from vision_models import ImagePayload, DetectedText, TextAnnotation
from vision_client import VisionClient

def detect_image_text(payload: ImagePayload, config: dict = None) -> DetectedText:
    config = config or {}
    client = VisionClient().get_image_annotator_client()

    image = vision.Image(content=payload.image_bytes)
    response = client.text_detection(image=image)

    if response.error.message:
        raise RuntimeError(response.error.message)

    texts = []
    if response.text_annotations:
        # The first annotation is the full text detected in the image
        full_text_annotation = response.text_annotations[0]
        # Other annotations are individual words or lines
        for text_annotation in response.text_annotations[1:]:
            texts.append(TextAnnotation(
                text=text_annotation.description,
                bounds=[{'x': v.x, 'y': v.y} for v in text_annotation.bounding_poly.vertices]
            ))

    return DetectedText(texts=texts)
