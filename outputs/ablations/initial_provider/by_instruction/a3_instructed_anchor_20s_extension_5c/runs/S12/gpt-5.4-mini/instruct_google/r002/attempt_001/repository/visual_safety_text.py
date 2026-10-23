from vision_client import analyze_safe_search
from vision_models import ImageAnalysisRequest


def visual_safety_text(text: str) -> bool:
    request = ImageAnalysisRequest(image_path=text)
    data = analyze_safe_search(request)
    return all(value in (None, 0, "UNKNOWN", "VERY_UNLIKELY", "UNLIKELY") for value in data.values())
