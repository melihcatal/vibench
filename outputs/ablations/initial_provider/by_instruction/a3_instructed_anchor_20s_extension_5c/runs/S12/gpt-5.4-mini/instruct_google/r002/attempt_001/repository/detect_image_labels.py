from vision_client import analyze_labels
from vision_models import ImageAnalysisRequest, normalize_labels


def detect_image_labels(image_path: str, max_results: int = 10):
    request = ImageAnalysisRequest(image_path=image_path, max_results=max_results)
    return normalize_labels(analyze_labels(request))
