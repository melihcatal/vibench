from azure.ai.vision.imageanalysis.models import VisualFeatures

def normalize_labels(result):
    return [{'name': tag.name, 'confidence': tag.confidence} for tag in result.tags.list]

def normalize_description(result):
    return result.caption.text if result.caption else 'No description available'

def normalize_text(result):
    return [line.text for line in result.text.lines]

def normalize_safety(result):
    return result.adult.is_adult_content