from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client, load_vision_config
from vision_models import normalize_safety


def score_image_safety(payload, config=None):
    config = load_vision_config(config)
    with build_client(config) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.OBJECTS])
    findings = []
    for obj in getattr(result, 'objects', []) or []:
        findings.append({'name': obj.tags[0].name if getattr(obj, 'tags', None) else obj.object_property, 'score': obj.confidence})
    return {'safety': normalize_safety(findings)}
