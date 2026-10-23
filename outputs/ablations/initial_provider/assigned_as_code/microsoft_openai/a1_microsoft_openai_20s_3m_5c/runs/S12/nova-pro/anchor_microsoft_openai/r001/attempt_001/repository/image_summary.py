from vision_client import get_vision_client
from vision_models import normalize_labels, normalize_description, normalize_text, normalize_safety


def image_summary(payload, config=None):
    config = config or {}
    client = get_vision_client(config)
    labels_result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.TAGS])
    description_result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.CAPTION])
    text_result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.TEXT])
    safety_result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.SAFETY])
    labels = normalize_labels(labels_result)
    description = normalize_description(description_result)
    text = normalize_text(text_result)
    safety = normalize_safety(safety_result)
    return {'labels': labels, 'description': description, 'text': text, 'safety': safety}