from vision_client import ensure_api_key, run_vision_request
from vision_models import VisionImageRequest


def detect_image_labels(image_path: str):
    ensure_api_key()
    request = VisionImageRequest(
        image_path=image_path,
        prompt="Identify the main objects and labels visible in this image. Return a concise list.",
    )
    return run_vision_request(request).labels
