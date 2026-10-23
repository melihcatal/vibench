from typing import List, Dict, Any

def normalize_rekognition_labels(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalizes the response from AWS Rekognition detect_labels.
    """
    labels = []
    for label in response.get('Labels', []):
        labels.append({
            'name': label.get('Name'),
            'confidence': label.get('Confidence')
        })
    return labels

def normalize_google_vision_labels(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalizes the response from Google Cloud Vision label_detection.
    """
    labels = []
    for label in response.label_annotations:
        labels.append({
            'description': label.description,
            'score': label.score
        })
    return labels

def normalize_google_vision_text(response: Dict[str, Any]) -> str:
    """
    Normalizes the response from Google Cloud Vision text_detection.
    """
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""

def normalize_google_vision_safety(response: Dict[str, Any]) -> Dict[str, str]:
    """
    Normalizes the response from Google Cloud Vision safe_search_detection.
    """
    safe_search_annotation = response.safe_search_annotation
    safety_scores = {
        'adult': safe_search_annotation.adult.name,
        'spoof': safe_search_annotation.spoof.name,
        'medical': safe_search_annotation.medical.name,
        'violence': safe_search_annotation.violence.name,
        'racy': safe_search_annotation.racy.name,
    }
    return safety_scores
