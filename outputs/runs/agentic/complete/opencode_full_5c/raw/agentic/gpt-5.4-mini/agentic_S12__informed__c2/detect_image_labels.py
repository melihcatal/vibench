import sys

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image, load_azure_vision_client
from vision_models import VisionRequest, normalize_labels


def detect_image_labels(image_path: str):
    client = load_azure_vision_client()
    request = VisionRequest(image_path=image_path)
    payload = analyze_image(
        client, request.image_path, [VisualFeatures.TAGS, VisualFeatures.OBJECTS]
    )
    return normalize_labels(payload)


if __name__ == "__main__":
    print(detect_image_labels(sys.argv[1]))
