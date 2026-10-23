from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import open_image_client, load_vision_config


def describe_image(payload, config=None):
    cfg = load_vision_config(config)
    with open_image_client(cfg) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.CAPTION])
    caption = getattr(result.caption, 'text', '') if getattr(result, 'caption', None) else ''
    return {'description': caption, 'confidence': getattr(result.caption, 'confidence', 0.0) if getattr(result, 'caption', None) else 0.0}
