import sys

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image, load_azure_vision_client
from vision_models import VisionRequest, normalize_safety


def score_image_safety(image_path: str):
    client = load_azure_vision_client()
    request = VisionRequest(image_path=image_path)
    payload = analyze_image(
        client, request.image_path, [VisualFeatures.OBJECTS, VisualFeatures.TAGS]
    )
    return normalize_safety(payload)


if __name__ == "__main__":
    print(score_image_safety(sys.argv[1]))
