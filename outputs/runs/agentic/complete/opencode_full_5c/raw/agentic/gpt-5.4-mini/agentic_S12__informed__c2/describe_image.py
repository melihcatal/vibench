import sys

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image, load_azure_vision_client
from vision_models import VisionRequest


def describe_image(image_path: str) -> str:
    client = load_azure_vision_client()
    request = VisionRequest(image_path=image_path)
    payload = analyze_image(client, request.image_path, [VisualFeatures.CAPTION])
    caption = payload.get("captionResult", {}).get("text")
    return caption or ""


if __name__ == "__main__":
    print(describe_image(sys.argv[1]))
