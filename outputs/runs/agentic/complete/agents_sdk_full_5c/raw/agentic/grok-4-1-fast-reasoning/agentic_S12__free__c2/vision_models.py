from typing import Dict, Any, List
from google.cloud.vision_v1 import AnnotateImageResponse

def normalize_labels(response: AnnotateImageResponse) -> Dict[str, Any]:
    if not response.label_annotations:
        return {"labels": [], "confidence_scores": []}
    labels = [la.description for la in response.label_annotations]
    scores = [float(la.score) for la in response.label_annotations]
    return {"labels": labels[:10], "confidence_scores": scores[:10]}

def normalize_text(response: AnnotateImageResponse) -> Dict[str, Any]:
    annotation = response.full_text_annotation
    if not annotation:
        return {"text": ""}
    return {"text": annotation.text}

def normalize_safety(response: AnnotateImageResponse) -> Dict[str, Any]:
    ss = response.safe_search_annotation
    if not ss:
        return {}
    return {
        "adult": ss.adult,
        "racy": ss.racy,
        "violence": ss.violence,
        "medical": ss.medical,
    }
