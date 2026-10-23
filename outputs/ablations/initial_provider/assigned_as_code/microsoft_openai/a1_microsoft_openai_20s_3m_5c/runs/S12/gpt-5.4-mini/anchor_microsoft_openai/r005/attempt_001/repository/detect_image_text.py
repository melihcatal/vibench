from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config, require_image_bytes
from vision_models import normalize_text_lines


def detect_image_text(payload, config=None):
    cfg = load_vision_config(config)
    image_bytes = require_image_bytes(payload)
    with ImageAnalysisClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key'])) as client:
        result = client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.READ])
    lines = []
    for block in getattr(result.read, 'blocks', []):
        lines.extend(getattr(block, 'lines', []))
    return {'text': normalize_text_lines(lines, cfg['max_words'])}
