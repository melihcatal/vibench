from vision_client import load_image_bytes, get_azure_vision_client
from vision_models import parse_azure_caption
from azure.ai.vision.imageanalysis import VisualFeatures


def describe_image(image_path: str) -> dict:
    image_bytes = load_image_bytes(image_path)
    client = get_azure_vision_client()
    result = client.analyze(
        image_bytes=image_bytes, visual_features=[VisualFeatures.CAPTION]
    )
    return parse_azure_caption(result)
