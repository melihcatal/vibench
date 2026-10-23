from vision_client import analyze_safe_search
from vision_models import ImageAnalysisRequest, SafetyResult


def score_image_safety(image_path: str) -> SafetyResult:
    request = ImageAnalysisRequest(image_path=image_path)
    data = analyze_safe_search(request)
    safe = all(value in (None, 0, "UNKNOWN", "VERY_UNLIKELY", "UNLIKELY") for value in data.values())
    return SafetyResult(safe=safe, categories=data)
