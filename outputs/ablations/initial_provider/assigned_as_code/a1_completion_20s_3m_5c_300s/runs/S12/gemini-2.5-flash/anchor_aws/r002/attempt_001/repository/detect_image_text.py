import boto3
from typing import Dict, Any
from vision_client import get_rekognition_client
from vision_models import ImagePayload, DetectTextResponse, TextDetection

def detect_image_text(payload: ImagePayload, config: Dict[str, Any]) -> DetectTextResponse:
    client = get_rekognition_client(config)
    image_bytes = payload.image_bytes

    response = client.detect_text(
        Image={'Bytes': image_bytes}
    )

    text_detections = []
    for text_detection in response.get('TextDetections', []):
        if text_detection['Type'] == 'WORD': # or 'LINE' depending on desired granularity
            text_detections.append(TextDetection(
                detected_text=text_detection['DetectedText'],
                confidence=text_detection['Confidence'] / 100.0,
                bounding_box=text_detection['Geometry']['BoundingBox']
            ))
    
    return DetectTextResponse(text_detections=text_detections)
