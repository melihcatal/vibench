from azure.ai.vision.imageanalysis.models import VisualFeatures

def normalize_labels(result):
    return [{'name': tag.name, 'confidence': tag.confidence} for tag in result.tags.list]

def normalize_description(result):
    return result.caption.content

def normalize_text(result):
    return [line.content for line in result.text.lines]

def normalize_safety_score(result):
    return result.adult.is_adult_content