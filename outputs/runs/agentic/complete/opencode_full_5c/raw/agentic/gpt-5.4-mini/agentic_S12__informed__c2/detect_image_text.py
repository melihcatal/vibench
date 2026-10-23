import sys

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image, load_azure_vision_client
from vision_models import VisionRequest, normalize_text


def detect_image_text(image_path: str) -> str:
    client = load_azure_vision_client()
    request = VisionRequest(image_path=image_path)
    payload = analyze_image(client, request.image_path, [VisualFeatures.READ])
    return normalize_text(payload)


if __name__ == "__main__":
    print(detect_image_text(sys.argv[1]))
