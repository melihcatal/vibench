from vision_client import ensure_api_key, run_vision_request
from vision_models import VisionImageRequest


def detect_image_text(image_path: str):
    ensure_api_key()
    request = VisionImageRequest(
        image_path=image_path,
        prompt="Read any text visible in this image and return it verbatim.",
    )
    return run_vision_request(request).texts
