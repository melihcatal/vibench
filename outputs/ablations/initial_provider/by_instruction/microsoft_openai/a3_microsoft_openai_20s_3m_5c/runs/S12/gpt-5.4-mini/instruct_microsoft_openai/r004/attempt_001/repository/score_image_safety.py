from vision_client import load_vision_config, run_vision_request
from vision_models import VisionRequest, normalize_text


def score_image_safety(image_path: str) -> str:
    cfg = load_vision_config()
    req = VisionRequest(
        image_path=image_path,
        prompt="Assess whether the image contains unsafe, violent, explicit, self-harm, hateful, or otherwise policy-sensitive visual content. Return a brief safety assessment.",
        model=cfg["model"],
        max_tokens=160,
    )
    return normalize_text(run_vision_request(req).text)
