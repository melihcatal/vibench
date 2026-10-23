from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import open_image_client, load_vision_config


def score_image_safety(payload, config=None):
    cfg = load_vision_config(config)
    with open_image_client(cfg) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.IMAGE_TYPE, VisualFeatures.PEOPLE, VisualFeatures.SMART_CROPS])
    people = getattr(result, 'people', None)
    adults = getattr(people, 'adult', []) if people else []
    racy = getattr(result, 'adult', None)
    if racy is None and hasattr(result, 'is_adult_content'):
        racy = result.is_adult_content
    return {'unsafe': bool(getattr(result, 'is_adult_content', False) or getattr(result, 'is_racy_content', False) or getattr(result, 'is_gory_content', False)), 'signals': {'adult': getattr(result, 'is_adult_content', False), 'racy': getattr(result, 'is_racy_content', False), 'gory': getattr(result, 'is_gory_content', False), 'people': len(adults)}}
