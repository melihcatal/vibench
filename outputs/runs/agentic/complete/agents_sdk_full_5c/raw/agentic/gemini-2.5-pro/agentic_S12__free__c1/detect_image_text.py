from typing import List
from azure.ai.vision.imageanalysis import VisualFeatures

from vision_client import get_azure_vision_client
from vision_models import DetectedText


def detect_text_in_image(image_bytes: bytes) -> List[DetectedText]:
    """
    Detects and extracts text from an image using Azure AI Vision (OCR).

    Args:
        image_bytes: The byte content of the image.

    Returns:
        A list of DetectedText objects.
    """
    vision_client = get_azure_vision_client()
    
    result = vision_client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.TEXT],
    )

    detected_texts = []
    if result.text is not None:
        for line in result.text.lines:
            # Flatten the polygon to a simple bounding box
            min_x = min(p.x for p in line.bounding_polygon)
            max_x = max(p.x for p in line.bounding_polygon)
            min_y = min(p.y for p in line.bounding_polygon)
            max_y = max(p.y for p in line.bounding_polygon)
            
            detected_texts.append(
                DetectedText(
                    text=line.text,
                    bounding_box=[min_x, min_y, max_x, max_y],
                    confidence=1.0 # Azure OCR API does not provide confidence score per line
                )
            )
            
    return detected_texts
