from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image


def score_image_safety(payload, config=None):
    result = analyze_image(payload, config or {}, [VisualFeatures.OBJECTS, VisualFeatures.TAGS, VisualFeatures.PEOPLE])
    people = getattr(result, 'people', None)
    objects = getattr(result, 'objects', None)
    tags = getattr(result, 'tags', None)
    score = 0.0
    if people and getattr(people, 'list', None):
        score += 0.5
    if objects and getattr(objects, 'list', None):
        score += 0.25
    if tags and getattr(tags, 'list', None):
        score += 0.25
    return {'unsafe_score': min(score, 1.0)}
