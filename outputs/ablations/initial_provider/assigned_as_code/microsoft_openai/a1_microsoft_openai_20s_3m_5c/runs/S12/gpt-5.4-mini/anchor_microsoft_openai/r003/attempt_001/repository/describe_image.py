from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client, load_vision_config


def describe_image(payload, config=None):
    config = load_vision_config(config)
    with build_client(config) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.CAPTION])
    caption = result.caption.text if result.caption else ''
    confidence = result.caption.confidence if result.caption else 0.0
    return {'description': {'text': caption, 'confidence': confidence}}
