from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image
from vision_models import normalize_text


def detect_image_text(payload, config=None):
    result = analyze_image(payload, config or {}, [VisualFeatures.READ])
    lines = []
    read = getattr(result, 'read', None)
    if read and getattr(read, 'blocks', None):
        for block in read.blocks:
            for line in getattr(block, 'lines', []) or []:
                lines.append({'text': normalize_text(getattr(line, 'text', '')), 'confidence': getattr(line, 'confidence', None)})
    return {'text': lines}
