from vision_client import load_vision_config, run_vision_request
from vision_models import VisionRequest, normalize_text


def detect_image_text(image_path: str) -> str:
    cfg = load_vision_config()
    req = VisionRequest(
        image_path=image_path,
        prompt="Extract all readable text from the image. Preserve line breaks where helpful.",
        model=cfg["model"],
        max_tokens=200,
    )
    return normalize_text(run_vision_request(req).text)
