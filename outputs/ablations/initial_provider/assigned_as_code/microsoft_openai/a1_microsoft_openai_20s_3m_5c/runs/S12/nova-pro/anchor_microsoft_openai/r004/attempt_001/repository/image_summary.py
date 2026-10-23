from vision_client import VisionClient


def image_summary(payload, config=None):
    config = config or {}
    client = VisionClient(config['endpoint'], config['api_key'])
    labels = client.detect_labels(payload['image_bytes'], config.get('max_labels', 10))
    description = client.describe_image(payload['image_bytes'])
    text = client.detect_text(payload['image_bytes'])
    safety = client.score_safety(payload['image_bytes'])
    return {'labels': labels, 'description': description, 'text': text, 'safety': safety}