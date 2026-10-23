from google.cloud import vision

def create_image_from_bytes(image_bytes):
    return vision.Image(content=image_bytes)

def create_feature(feature_type, max_results=None):
    feature = vision.Feature(type=feature_type)
    if max_results:
        feature.max_results = max_results
    return feature

def parse_label_detection_response(response):
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append({'name': label.description, 'confidence': label.score})
    return labels

def parse_text_detection_response(response):
    texts = []
    if response.text_annotations:
        for text in response.text_annotations:
            texts.append({'text': text.description, 'confidence': text.score if hasattr(text, 'score') else None})
    return texts

def parse_safe_search_detection_response(response):
    safe_search_annotation = response.safe_search_annotation
    if safe_search_annotation:
        return {
            'adult': safe_search_annotation.adult.name,
            'spoof': safe_search_annotation.spoof.name,
            'medical': safe_search_annotation.medical.name,
            'violence': safe_search_annotation.violence.name,
            'racy': safe_search_annotation.racy.name,
        }
    return {}

def parse_web_detection_response(response):
    web_detection = response.web_detection
    web_entities = []
    if web_detection and web_detection.web_entities:
        for entity in web_detection.web_entities:
            web_entities.append({'description': entity.description, 'score': entity.score})
    return web_entities
