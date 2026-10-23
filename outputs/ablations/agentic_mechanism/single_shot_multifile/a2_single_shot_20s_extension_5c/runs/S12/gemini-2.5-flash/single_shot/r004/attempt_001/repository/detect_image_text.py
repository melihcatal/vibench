import os
import base64
from google.cloud import vision_v1p3beta1 as vision
from vision_models import ImageInput, TextDetectionResult

def detect_image_text(image_input: ImageInput) -> TextDetectionResult:
    client = vision.ImageAnnotatorClient()

    if image_input.content_base64:
        image = vision.Image(content=base64.b64decode(image_input.content_base64))
    elif image_input.image_uri:
        image = vision.Image(source=vision.ImageSource(image_uri=image_input.image_uri))
    else:
        raise ValueError("ImageInput must contain either content_base64 or image_uri")

    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts_list = []
    full_text = ""

    if texts:
        full_text = texts[0].description
        # Skip the first element as it contains the aggregated full text
        for text_annotation in texts[1:]:
            detected_texts_list.append({
                'text': text_annotation.description,
                'bounds': [{'x': v.x, 'y': v.y} for v in text_annotation.bounding_poly.vertices]
            })

    return TextDetectionResult(full_text=full_text, detected_texts=detected_texts_list)