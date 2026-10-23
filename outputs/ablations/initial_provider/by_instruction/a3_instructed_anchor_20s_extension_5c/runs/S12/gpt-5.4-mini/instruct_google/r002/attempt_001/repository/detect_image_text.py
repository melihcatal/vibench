from vision_client import analyze_text
from vision_models import ImageAnalysisRequest, normalize_text_blocks


def detect_image_text(image_path: str):
    request = ImageAnalysisRequest(image_path=image_path)
    return normalize_text_blocks(analyze_text(request))
