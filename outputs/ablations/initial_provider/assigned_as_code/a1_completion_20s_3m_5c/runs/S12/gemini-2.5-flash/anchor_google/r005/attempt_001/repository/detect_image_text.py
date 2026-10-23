from google.cloud import vision
from vision_client import get_image_annotator_client
from vision_models import VisionRequest, ImageResponse, DetectedText

def detect_image_text(payload, config=None):
    config = config or {}
    client = get_image_annotator_client()
    image = vision.Image(content=payload["image_bytes"])

    response = client.text_detection(image=image)

    if response.error.message:
        raise RuntimeError(response.error.message)
    
    # The first text annotation is usually the full text detected in the image.
    # Subsequent annotations are individual words or lines.
    texts = []
    if response.text_annotations:
        for text_annotation in response.text_annotations:
            texts.append(DetectedText(
                text=text_annotation.description,
                bounds=[
                    {"x": v.x, "y": v.y} 
                    for v in text_annotation.bounding_poly.vertices
                ]
            ))
    
    # Return the full text description as well
    full_text = response.full_text_annotation.text if response.full_text_annotation else ""

    return {"full_text": full_text, "detected_texts": [t.__dict__ for t in texts]}
