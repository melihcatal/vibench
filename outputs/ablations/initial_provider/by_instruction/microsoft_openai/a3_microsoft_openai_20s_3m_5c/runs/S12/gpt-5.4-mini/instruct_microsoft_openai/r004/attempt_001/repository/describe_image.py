from vision_client import load_vision_config, run_vision_request
from vision_models import VisionRequest, normalize_text


def describe_image(image_path: str) -> str:
    cfg = load_vision_config()
    req = VisionRequest(
        image_path=image_path,
        prompt="Write one short, natural-language sentence describing the image.",
        model=cfg["model"],
        max_tokens=120,
    )
    return normalize_text(run_vision_request(req).text)
