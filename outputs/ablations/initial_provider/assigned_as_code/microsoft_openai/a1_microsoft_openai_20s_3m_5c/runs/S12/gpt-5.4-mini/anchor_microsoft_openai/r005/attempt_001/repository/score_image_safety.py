from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config, require_image_bytes
from vision_models import normalize_safety_result


def score_image_safety(payload, config=None):
    cfg = load_vision_config(config)
    image_bytes = require_image_bytes(payload)
    with ImageAnalysisClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key'])) as client:
        result = client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.PEOPLE, VisualFeatures.TAGS])
    categories = []
    for tag in getattr(result, 'tags', []).list:
        if tag.confidence and tag.confidence > 0.8:
            categories.append({'name': tag.name, 'confidence': tag.confidence})
    return {'safety': normalize_safety_result(True, categories)}
