from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_client, load_vision_config
from vision_models import normalize_text_lines


def detect_image_text(payload, config=None):
    config = load_vision_config(config)
    with build_client(config) as client:
        result = client.analyze(image_data=payload['image_bytes'], visual_features=[VisualFeatures.READ])
    lines = []
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                lines.append({'text': line.text, 'confidence': getattr(line, 'confidence', 1.0)})
    return {'text': normalize_text_lines(lines)}
