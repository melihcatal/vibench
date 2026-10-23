from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config
from vision_models import normalize_safety


def score_image_safety(image_url: str):
    config = load_vision_config()
    client = ImageAnalysisClient(config.endpoint, AzureKeyCredential(config.api_key))
    result = client.analyze_from_url(image_url=image_url, visual_features=["adult"])
    flags = {
        "adult": getattr(getattr(result, "adult", None), "is_adult_content", None),
        "racy": getattr(getattr(result, "adult", None), "is_racy_content", None),
        "gory": getattr(getattr(result, "adult", None), "is_gory_content", None),
        "violence": getattr(
            getattr(result, "adult", None), "is_violence_content", None
        ),
    }
    return normalize_safety(flags)
