from typing import Dict, List, Any


def normalize_vision_labels(response_labels: List[Any]) -> List[str]:
    return [label.description for label in response_labels]


def normalize_vision_safe_search(response_safe_search: Any) -> Dict[str, str]:
    return {
        "adult": response_safe_search.adult.name,
        "spoof": response_safe_search.spoof.name,
        "medical": response_safe_search.medical.name,
        "violence": response_safe_search.violence.name,
        "racy": response_safe_search.racy.name,
    }


def normalize_vision_text(response_texts: List[Any]) -> str:
    if response_texts:
        return response_texts[0].description
    return ""
