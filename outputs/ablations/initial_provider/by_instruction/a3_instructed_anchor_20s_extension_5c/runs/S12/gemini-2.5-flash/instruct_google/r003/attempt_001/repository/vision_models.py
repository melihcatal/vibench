import base64
from typing import List, Dict, Any

def image_to_base64(image_path: str) -> str:
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def normalize_text_detection_response(response: Any) -> Dict[str, Any]:
    texts = []
    full_text = ""
    if response.text_annotations:
        full_text = response.text_annotations[0].description # The first annotation is the full text
        for i, text in enumerate(response.text_annotations):
            if i == 0: # Skip the first one as it is the full text
                continue
            texts.append({
                'description': text.description,
                'bounding_poly': [
                    {'x': v.x, 'y': v.y} for v in text.bounding_poly.vertices
                ]
            })
    return {'full_text': full_text, 'texts': texts}

def normalize_safe_search_detection_response(response: Any) -> Dict[str, str]:
    safe_search_annotation = response.safe_search_annotation
    return {
        'adult': safe_search_annotation.adult.name,
        'spoof': safe_search_annotation.spoof.name,
        'medical': safe_search_annotation.medical.name,
        'violence': safe_search_annotation.violence.name,
        'racy': safe_search_annotation.racy.name,
    }



def normalize_label_detection_response(response: Any) -> List[Dict[str, Any]]:
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append({
                'description': label.description,
                'score': label.score,
                'topicality_score': label.topicality_score
            })
    return labels
