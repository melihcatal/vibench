import os
from google.cloud import vision

def detect_image_text(image_bytes: bytes) -> dict:
    """
    Detects text appearing inside an image using Google Cloud Vision API.

    Args:
        image_bytes: The image content in bytes.

    Returns:
        A dictionary containing the detected text.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    detected_text = []
    if texts:
        # The first annotation is the overall text detected in the image
        full_text = texts[0].description
        detected_text.append({'full_text': full_text})
        
        # You can also get individual words/lines if needed
        # for text in texts[1:]:
        #     detected_text.append({'text': text.description, 'bounds': text.bounding_poly})
            
    return {'detected_text': detected_text}
