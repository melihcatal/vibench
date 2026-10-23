# [HELPER] translation_models.py
from typing import Dict, Any, List

def normalize_translation_response(resp: Dict[str, Any]) -> str:
    """Extract translated text from Google Translation API response."""
    return resp.get('translatedText', '')


def build_translation_request(texts: List[str], target_language: str = 'en') -> Dict[str, Any]:
    """Prepare payload for bulk translation using Google API."""
    return {
        'q': texts,
        'target': target_language,
    }
