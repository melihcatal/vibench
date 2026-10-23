from azure.ai.vision.imageanalysis.models import VisualFeatures


def normalize_labels(result):
    return [{'name': tag.name, 'confidence': tag.confidence} for tag in result.tags.list]


def normalize_description(result):
    return result.caption.content


def normalize_text(response):
    return ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])


def normalize_safety(response):
    return {'adult': response.safe_search_annotation.adult, 'spoof': response.safe_search_annotation.spoof, 'medical': response.safe_search_annotation.medical, 'violence': response.safe_search_annotation.violence}