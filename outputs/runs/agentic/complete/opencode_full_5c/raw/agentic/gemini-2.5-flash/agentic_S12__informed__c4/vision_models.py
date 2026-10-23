from typing import List, Dict, Any


def normalize_labels_response(response: Any) -> List[Dict[str, Any]]:
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append({"description": label.description, "score": label.score})
    return labels


def normalize_text_detection_response(response: Any) -> str:
    if response.text_annotations:
        return response.text_annotations[0].description
    return ""


def normalize_safe_search_response(response: Any) -> Dict[str, str]:
    safe_search_annotation = response.safe_search_annotation
    return {
        "adult": safe_search_annotation.adult.name,
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }


def normalize_image_description(labels: List[Dict[str, Any]]) -> str:
    descriptions = [label["description"] for label in labels if label["score"] > 0.7]
    if descriptions:
        return "An image containing: " + ", ".join(descriptions) + "."
    return "An image with no clear description."
