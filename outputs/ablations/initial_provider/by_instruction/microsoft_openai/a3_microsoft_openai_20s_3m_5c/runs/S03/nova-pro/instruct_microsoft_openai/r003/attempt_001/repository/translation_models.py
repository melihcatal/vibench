from typing import Any, Dict, List

def normalize_request(text: str, source_language: str, target_language: str) -> Dict[str, Any]:
    return {
        'text': text,
        'source_language': source_language,
        'target_language': target_language
    }

def normalize_response(response: Dict[str, Any]) -> str:
    return response['translatedText']