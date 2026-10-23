from vision_client import ensure_api_key, run_vision_request
from vision_models import VisionImageRequest


def describe_image(image_path: str):
    ensure_api_key()
    request = VisionImageRequest(
        image_path=image_path,
        prompt="Write a short visual description of this image.",
    )
    return run_vision_request(request).content
