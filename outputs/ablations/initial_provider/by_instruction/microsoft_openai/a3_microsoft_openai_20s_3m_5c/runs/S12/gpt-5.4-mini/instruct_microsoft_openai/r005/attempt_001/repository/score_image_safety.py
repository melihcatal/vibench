from vision_client import analyze_image
from vision_models import VisionRequest


def score_image_safety(image_path: str):
    request = VisionRequest(image_path=image_path, prompt='Return JSON with an "unsafe" boolean indicating whether the image contains unsafe or policy-sensitive visual content.')
    return analyze_image(request).unsafe
