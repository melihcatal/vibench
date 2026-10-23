from vision_client import analyze_image
from vision_models import VisionRequest


def detect_image_labels(image_path: str):
    request = VisionRequest(image_path=image_path, prompt='Return JSON with a "labels" array of the main objects and entities visible in the image.')
    return analyze_image(request).labels
