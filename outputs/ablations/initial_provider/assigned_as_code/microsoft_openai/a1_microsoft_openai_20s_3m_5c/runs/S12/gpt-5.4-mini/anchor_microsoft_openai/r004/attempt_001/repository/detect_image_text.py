from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import open_image_client, load_vision_config


def detect_image_text(payload, config=None):
    cfg = load_vision_config(config)
    with open_image_client(cfg) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.READ])
    lines = []
    for block in getattr(result.read, 'blocks', []) or []:
        for line in getattr(block, 'lines', []) or []:
            lines.append({'text': line.text, 'confidence': getattr(line, 'confidence', 0.0)})
    return {'text': lines[:int(cfg.get('max_text_items', 20))]}
