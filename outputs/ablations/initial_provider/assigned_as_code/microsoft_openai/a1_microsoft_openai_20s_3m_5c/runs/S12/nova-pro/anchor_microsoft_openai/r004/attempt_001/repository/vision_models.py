from azure.ai.vision.imageanalysis.models import VisualFeatures


def normalize_payload(payload):
    return {'image_bytes': payload['image_bytes'], 'config': payload.get('config', {})}


def parse_labels_response(response):
    return [{'name': tag.name, 'confidence': tag.confidence} for tag in response.tags.list]


def parse_description_response(response):
    return response.caption.text


def parse_text_response(response):
    text_regions = response.text.regions
    return ' '.join([line.text for region in text_regions for line in region.lines])


def parse_safety_response(response):
    adult_content = response.adult.is_adult_content
    racy_content = response.adult.is_racy_content
    safety_score = 0
    if not adult_content and not racy_content:
        safety_score = 100
    return {'safety_score': safety_score, 'is_safe': not adult_content and not racy_content}