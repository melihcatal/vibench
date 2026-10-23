from vision_client import analyze_image
from vision_models import VisionRequest


def detect_image_text(image_path: str):
    request = VisionRequest(image_path=image_path, prompt='Return JSON with a "text" array containing all readable text in the image.')
    return analyze_image(request).text
