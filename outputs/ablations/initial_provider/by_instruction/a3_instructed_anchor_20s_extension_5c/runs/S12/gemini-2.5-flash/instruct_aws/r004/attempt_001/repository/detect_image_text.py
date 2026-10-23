from typing import List, Dict, Any
from vision_client import get_rekognition_client
from vision_models import DetectedText, DetectTextResponse

def detect_image_text(image_bytes: bytes) -> DetectTextResponse:
    """
    Detects text appearing inside an image using AWS Rekognition.

    Args:
        image_bytes: The image content as bytes.

    Returns:
        A DetectTextResponse object containing the detected text.
    """
    rekognition_client = get_rekognition_client()
    
    response = rekognition_client.detect_text(
        Image={'Bytes': image_bytes}
    )

    text_detections = []
    for text_data in response.get('TextDetections', []):
        if text_data.get('Type') == 'LINE': # Only process lines of text
            text = DetectedText(
                text=text_data.get('DetectedText'),
                confidence=text_data.get('Confidence'),
                bounding_box=text_data.get('Geometry', {}).get('BoundingBox', {})
            )
            text_detections.append(text)
    
    return DetectTextResponse(text_detections=text_detections)
