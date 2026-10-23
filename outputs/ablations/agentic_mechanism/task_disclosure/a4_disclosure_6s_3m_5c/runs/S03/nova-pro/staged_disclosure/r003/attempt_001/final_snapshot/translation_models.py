from typing import Dict, Any


def create_translation_request(text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
    return {
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }


def parse_translation_response(response: Dict[str, Any]) -> str:
    return response.get('translated_text', '')


def normalize_text(text: str) -> str:
    return text.strip().lower()