from typing import List, Dict, Any

def create_text_translation_payload(text: str, source_language: str, target_language: str) -> Dict[str, str]:
    return {
        "text": text,
        "source_language": source_language,
        "target_language": target_language,
    }

def create_batch_translation_payload(texts: List[str], source_language: str, target_language: str) -> Dict[str, Any]:
    return {
        "texts": texts,
        "source_language": source_language,
        "target_language": target_language,
    }

def create_markup_translation_payload(markup: str, source_language: str, target_language: str) -> Dict[str, str]:
    return {
        "markup": markup,
        "source_language": source_language,
        "target_language": target_language,
    }

def create_dictionary_translation_payload(dictionary: Dict[str, str], source_language: str, target_language: str) -> Dict[str, Any]:
    return {
        "dictionary": dictionary,
        "source_language": source_language,
        "target_language": target_language,
    }

def create_comprehend_text_payload(text: str, language_code: str) -> Dict[str, str]:
    return {
        "text": text,
        "language_code": language_code
    }

def create_polly_synthesis_payload(text: str, voice_id: str, output_format: str = "mp3") -> Dict[str, str]:
    return {
        "text": text,
        "voice_id": voice_id,
        "output_format": output_format
    }