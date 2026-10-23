from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_azure_vision_client
from vision_models import normalize_texts, VisionTexts

def detect_image_text(image_path: str) -&gt; VisionTexts:
    client = get_azure_vision_client()
    result = client.analyze(image_path, features=[VisualFeatures.READ])
    return normalize_texts(result)