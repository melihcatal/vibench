from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import analyze_image


def image_summary(payload, config=None):
    result = analyze_image(payload, config or {}, [VisualFeatures.CAPTION, VisualFeatures.TAGS])
    caption = getattr(result.caption, 'text', '') if getattr(result, 'caption', None) else ''
    tags = []
    for tag in getattr(getattr(result, 'tags', None), 'list', []) or []:
        tags.append(getattr(tag, 'name', ''))
    return {'summary': caption, 'tags': tags[:5]}
