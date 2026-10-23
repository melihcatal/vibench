from vision_client import analyze_image
from vision_models import VisionRequest


def describe_image(image_path: str):
    request = VisionRequest(image_path=image_path, prompt='Return JSON with a short "description" of the image in one sentence.')
    return analyze_image(request).description
