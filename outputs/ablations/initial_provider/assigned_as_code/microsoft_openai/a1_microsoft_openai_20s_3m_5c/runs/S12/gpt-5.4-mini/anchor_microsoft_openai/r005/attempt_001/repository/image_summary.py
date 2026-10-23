from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config, require_image_bytes


def image_summary(payload, config=None):
    cfg = load_vision_config(config)
    image_bytes = require_image_bytes(payload)
    with ImageAnalysisClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key'])) as client:
        result = client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS, VisualFeatures.READ])
    caption = result.caption.text if result.caption else ''
    labels = [tag.name for tag in getattr(result.tags, 'list', [])[:cfg['max_labels']]]
    return {'summary': {'caption': caption, 'labels': labels}}
