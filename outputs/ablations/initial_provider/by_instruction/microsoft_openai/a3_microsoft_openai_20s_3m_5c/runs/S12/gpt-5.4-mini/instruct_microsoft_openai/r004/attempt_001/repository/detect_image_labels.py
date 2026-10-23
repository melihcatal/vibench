from vision_client import load_vision_config, run_vision_request
from vision_models import VisionRequest, normalize_items


def detect_image_labels(image_path: str):
    cfg = load_vision_config()
    req = VisionRequest(
        image_path=image_path,
        prompt="List the main objects, subjects, and scene labels visible in this image as concise labels separated by commas.",
        model=cfg["model"],
        max_tokens=200,
    )
    return normalize_items(run_vision_request(req).text)
