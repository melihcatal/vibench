import base64
from pathlib import Path
from typing import List, Dict, Any

from vision_client import VisionClient
from vision_models import VisionModels


def score_image_safety(image_path: Path, provider: str = "google_vision") -> List[Dict[str, Any]]:
    """Check a static image for unsafe or policy‑sensitive visual content.\n    \n    Args:\n        image_path (Path): Path to the image file.\n        provider (str): Provider identifier (default: "google_vision").\n    \n    Returns:\n        List[Dict[str, Any]]: List of safety annotations (e.g., adult, medical, violence)\n        with confidence scores.\n    """
    # Load image bytes\n    image_bytes = image_path.read_bytes()

    # Provider client\n    client = VisionClient(provider)
    # For safety scoring we request the SAFE_SEARCH_DETECTION feature\n    request_payload = {
        "image": {
            "content": base64.b64encode(image_bytes).decode("utf-8")
        },
        "features": [
            {"type_": "SAFE_SEARCH_DETECTION"}
        ]
    }
    raw_response = client.annotate_image(request_payload)

    # Normalize response – each provider uses its own field names\n    if provider == "google_vision":
        return [
            {
                "category": annotation.safe_search_annotation.adult,
                "confidence": str(annotation.safe_search_annotation.adult_confidence)
            }
            for annotation in raw_response.safe_search_annotations
        ]
    elif provider == "aws_rekognition":
        return [
            {
                "category": label['Name'],
                "confidence": str(label['Confidence'])
            }
            for label in raw_response['Labels']
            if label['Name'] in ["EXPLICIT_NUDITY", "PARTIAL_NUDITY", "GRAPHIC_VIOLENCE", "SUGGESTIVE"]
        ]
    elif provider == "azure_vision":
        return [
            {
                "category": category['name'],
                "confidence": str(category['confidence'])
            }
            for category in raw_response['categories']
            if category['name'] in ["adult", "medical", "violence"]
        ]
    else:
        # Placeholder for other providers – return empty list\n        return []
