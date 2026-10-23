from typing import Dict, Any

def create_text_content_safety_request(text: str) -> Dict[str, Any]:
    return {
        'text': text
    }

def parse_text_content_safety_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'safety_score': response.get('safety_score', None),
        'categories': response.get('categories', [])
    }

def normalize_text_content_safety_score(score: float) -> float:
    return max(0, min(1, score))
