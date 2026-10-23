from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image


def describe_image(payload, config=None):
    result = analyze_image(payload, config or {}, [VisualFeatures.CAPTION])
    caption = getattr(result.caption, 'text', '') if getattr(result, 'caption', None) else ''
    return {'description': caption}
