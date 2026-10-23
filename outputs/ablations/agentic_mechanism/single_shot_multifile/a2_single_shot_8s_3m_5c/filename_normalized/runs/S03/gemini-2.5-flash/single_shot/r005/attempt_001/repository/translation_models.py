from typing import List, Dict, Any

def create_translation_request(
    text: str,
    source_language: str,
    target_language: str,
    mime_type: str = "text/plain"
) -> Dict[str, Any]:
    return {
        "text": text,
        "source_language": source_language,
        "target_language": target_language,
        "mime_type": mime_type
    }

def create_translation_result(
    original_text: str,
    translated_text: str,
    source_language: str,
    target_language: str
) -> Dict[str, Any]:
    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language
    }

def create_moderation_result(
    text: str,
    flagged: bool,
    categories: Dict[str, bool],
    category_scores: Dict[str, float]
) -> Dict[str, Any]:
    return {
        "text": text,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores
    }

def create_embedding_result(text: str, embedding: List[float]) -> Dict[str, Any]:
    return {"text": text, "embedding": embedding}

def create_audio_preview_result(text: str, audio_content_base64: str, language_code: str) -> Dict[str, Any]:
    return {"text": text, "audio_content_base64": audio_content_base64, "language_code": language_code}
