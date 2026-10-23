from typing import List, Dict, Any

class ImageRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

class ImageLabelResponse:
    def __init__(self, labels: List[Dict[str, Any]]):
        self.labels = labels

class ImageDescriptionResponse:
    def __init__(self, description: str):
        self.description = description

class ImageTextResponse:
    def __init__(self, text_detections: List[Dict[str, Any]]):
        self.text_detections = text_detections

class ImageSafetyResponse:
    def __init__(self, moderation_labels: List[Dict[str, Any]]):
        self.moderation_labels = moderation_labels

class ImageSummaryRequest:
    def __init__(self, text_to_summarize: str):
        self.text_to_summarize = text_to_summarize

class ImageSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary

class AltTextTranslateRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class AltTextTranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

class VisualSafetyTextRequest:
    def __init__(self, text: str):
        self.text = text

class VisualSafetyTextResponse:
    def __init__(self, is_unsafe: bool, reasons: List[str]):
        self.is_unsafe = is_unsafe
        self.reasons = reasons

class ImageAssetArchiveRequest:
    def __init__(self, bucket_name: str, key: str, data: bytes, content_type: str = 'application/octet-stream'):
        self.bucket_name = bucket_name
        self.key = key
        self.data = data
        self.content_type = content_type

class ImageAssetArchiveResponse:
    def __init__(self, archive_url: str):
        self.archive_url = archive_url

def normalize_rekognition_labels(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized_labels = []
    for label in response.get('Labels', []):
        normalized_labels.append({
            'name': label.get('Name'),
            'confidence': label.get('Confidence'),
            'parent_name': label.get('Parents')[0].get('Name') if label.get('Parents') else None
        })
    return normalized_labels

def normalize_rekognition_text(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized_text_detections = []
    for text_detection in response.get('TextDetections', []):
        normalized_text_detections.append({
            'detected_text': text_detection.get('DetectedText'),
            'type': text_detection.get('Type'),
            'confidence': text_detection.get('Confidence'),
        })
    return normalized_text_detections

def normalize_rekognition_moderation_labels(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized_moderation_labels = []
    for label in response.get('ModerationLabels', []):
        normalized_moderation_labels.append({
            'name': label.get('Name'),
            'parent_name': label.get('ParentName'),
            'confidence': label.get('Confidence'),
        })
    return normalized_moderation_labels

def normalize_comprehend_key_phrases(response: Dict[str, Any]) -> List[str]:
    return [phrase.get('Text') for phrase in response.get('KeyPhrases', [])]
