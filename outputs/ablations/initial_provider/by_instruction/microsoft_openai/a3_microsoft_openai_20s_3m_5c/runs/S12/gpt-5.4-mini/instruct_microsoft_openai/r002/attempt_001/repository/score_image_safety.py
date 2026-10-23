from vision_client import ensure_api_key, run_vision_request
from vision_models import VisionImageRequest


def score_image_safety(image_path: str):
    ensure_api_key()
    request = VisionImageRequest(
        image_path=image_path,
        prompt="Assess whether this image contains unsafe or policy-sensitive visual content. Return a brief safety judgment.",
    )
    return run_vision_request(request).safety or run_vision_request(request).content
