from vision_client import VisionClient
from vision_models import VisionImageInput


def score_image_safety(image_path: str):
    return VisionClient.from_env().score_safety(VisionImageInput(image_path=image_path))
