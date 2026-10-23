from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config, require_image_bytes
from vision_models import normalize_caption


def describe_image(payload, config=None):
    cfg = load_vision_config(config)
    image_bytes = require_image_bytes(payload)
    with ImageAnalysisClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key'])) as client:
        result = client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.CAPTION])
    caption = result.caption.text if result.caption else ''
    confidence = result.caption.confidence if result.caption else None
    return {'description': normalize_caption(caption, confidence)}
