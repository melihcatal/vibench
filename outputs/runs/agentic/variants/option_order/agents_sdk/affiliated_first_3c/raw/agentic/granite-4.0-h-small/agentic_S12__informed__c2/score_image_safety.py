# score_image_safety.py
from vision_client import VisionClient
from vision_models import SafetyCheckResponse

def score_image_safety(image_path: str) -> SafetyCheckResponse:
    client = VisionClient()
    # Azure AI Vision SDK example
    result = client.analyze_safety(image_path)
    return SafetyCheckResponse.from_sdk(result)
