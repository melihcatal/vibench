from typing import List, Dict, Optional, TypedDict


class TranslationRequest(TypedDict):
    text: str
    source_lang: str
    target_lang: str


class TranslationResponse(TypedDict):
    translated_text: str
    source_lang: str
    target_lang: str


def normalize_language_code(code: str) -> str:
    """Normalize language codes for Amazon Translate."""
    code = code.lower().replace('-', '_')
    if '_' in code:
        return code.split('_')[0]
    return code


def batch_requests_from_list(texts: List[str], source_lang: str, target_lang: str) -> List[TranslationRequest]:
    """Create batch requests from a list of texts."""
    return [
        {"text": text, "source_lang": source_lang, "target_lang": target_lang}
        for text in texts
    ]


def batch_responses_to_list(responses: List[Optional[TranslationResponse]]) -> List[str]:
    """Extract translated texts from batch responses."""
    return [resp["translated_text"] if resp else "" for resp in responses]