import os
from google.cloud import vision
from vision_models import ImageAnalysisRequest, TextDetectionResult

def detect_image_text(request: ImageAnalysisRequest) -> TextDetectionResult:
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = request.image_url

    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    if texts:
        # The first text annotation is the overall text detected in the image
        # Subsequent annotations are for individual words/lines, if available
        detected_texts = [text.description for text in texts[1:]] # Skip the first which is often the full text
        if texts[0].description: # Add the full text as well if it exists
            detected_texts.insert(0, texts[0].description)

    return TextDetectionResult(detected_text=detected_texts)
