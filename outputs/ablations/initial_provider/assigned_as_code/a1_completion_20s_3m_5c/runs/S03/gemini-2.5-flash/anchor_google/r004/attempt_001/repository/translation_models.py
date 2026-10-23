from typing import Dict, List, Any

def create_text_request(contents: List[str], source_language: str, target_language: str, mime_type: str = "text/plain") -> Dict[str, Any]:
    return {
        "contents": contents,
        "mime_type": mime_type,
        "source_language_code": source_language,
        "target_language_code": target_language,
    }

def parse_translation_response(response) -> List[str]:
    return [translation.translated_text for translation in response.translations]
