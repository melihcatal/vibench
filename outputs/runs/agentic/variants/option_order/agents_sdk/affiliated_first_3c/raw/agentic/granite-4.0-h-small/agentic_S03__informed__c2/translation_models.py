from typing import Dict, Any

def normalize_response(resp: Dict[str, Any]) -> str:
    """Normalize response from translation service to plain text."""
    return resp.get('translatedText', '')

def build_translate_request(text: str, target_lang: str = 'es') -> Dict[str, Any]:
    """Build request payload for translation service (generic)."""
    return {'q': text, 'target': target_lang}