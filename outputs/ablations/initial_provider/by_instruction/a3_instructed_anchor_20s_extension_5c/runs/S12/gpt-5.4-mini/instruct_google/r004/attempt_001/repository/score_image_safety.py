from google.cloud import vision

from vision_client import client, image_from_input
from vision_models import VisionAnalysisResult, VisionImageInput, normalize_safety


def score_image_safety(image_path: str = None, image_bytes: bytes = None) -> VisionAnalysisResult:
    vision_client = client()
    image = image_from_input(VisionImageInput(image_path=image_path, image_bytes=image_bytes))
    response = vision_client.safe_search_detection(image=image)
    findings = normalize_safety([
        {"category": "adult", "likelihood": str(response.safe_search_annotation.adult), "confidence": 0.0},
        {"category": "violence", "likelihood": str(response.safe_search_annotation.violence), "confidence": 0.0},
        {"category": "racy", "likelihood": str(response.safe_search_annotation.racy), "confidence": 0.0},
        {"category": "medical", "likelihood": str(response.safe_search_annotation.medical), "confidence": 0.0},
        {"category": "spoof", "likelihood": str(response.safe_search_annotation.spoof), "confidence": 0.0},
    ])
    return VisionAnalysisResult(provider="google-cloud-vision", kind="safety", raw=vision.ImageAnnotatorClient.to_dict(response), safety=findings)
