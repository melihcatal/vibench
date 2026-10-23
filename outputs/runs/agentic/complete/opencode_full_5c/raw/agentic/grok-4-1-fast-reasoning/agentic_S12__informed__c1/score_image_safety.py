from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_azure_vision_client
from vision_models import normalize_safety, VisionSafety

def score_image_safety(image_path: str) -&gt; VisionSafety:
    client = get_azure_vision_client()
    result = client.analyze(image_path, features=[VisualFeatures.ADULT_CONTENT])
    return normalize_safety(result)