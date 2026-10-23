from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_azure_vision_client
from vision_models import normalize_caption, VisionCaption

def describe_image(image_path: str) -&gt; VisionCaption:
    client = get_azure_vision_client()
    result = client.analyze(image_path, features=[VisualFeatures.CAPTION])
    return normalize_caption(result)