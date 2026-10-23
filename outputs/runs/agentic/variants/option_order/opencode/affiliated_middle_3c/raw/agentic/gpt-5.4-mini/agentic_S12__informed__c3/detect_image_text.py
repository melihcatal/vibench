from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config
from vision_models import normalize_text


def detect_image_text(image_url: str) -> str:
    config = load_vision_config()
    client = ImageAnalysisClient(config.endpoint, AzureKeyCredential(config.api_key))
    result = client.analyze_from_url(image_url=image_url, visual_features=["read"])
    lines = []
    for block in getattr(result, "read", []) or []:
        for line in getattr(block, "lines", []) or []:
            lines.append({"text": getattr(line, "text", "")})
    return normalize_text(lines)
