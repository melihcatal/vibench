from typing import List, Dict, Any, Optional

class TranslationRequest:
    """Represents a request for text translation."""
    def __init__(self, text: str, target_language: str, source_language: Optional[str] = None, format: Optional[str] = None):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language
        self.format = format # e.g., 'html' or 'text'

class TranslationResponse:
    """Represents a response from a text translation service."""
    def __init__(self, original_text: str, translated_text: str, detected_source_language: Optional[str] = None):
        self.original_text = original_text
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language

    @classmethod
    def from_google_cloud_translate_result(cls, original_text: str, result: Dict[str, Any]):
        """Normalizes a Google Cloud Translation result into a TranslationResponse object."""
        return cls(
            original_text=original_text,
            translated_text=result.get('translatedText', ''),
            detected_source_language=result.get('detectedSourceLanguage', None)
        )

class BatchTranslationRequest:
    """Represents a request for batch text translation."""
    def __init__(self, texts: List[str], target_language: str, source_language: Optional[str] = None):
        self.texts = texts
        self.target_language = target_language
        self.source_language = source_language

class BatchTranslationResponse:
    """Represents a response from a batch text translation service."""
    def __init__(self, original_texts: List[str], translated_texts: List[str], detected_source_languages: Optional[List[str]] = None):
        self.original_texts = original_texts
        self.translated_texts = translated_texts
        self.detected_source_languages = detected_source_languages

    @classmethod
    def from_google_cloud_translate_results(cls, original_texts: List[str], results: List[Dict[str, Any]]):
        """Normalizes Google Cloud Translation results into a BatchTranslationResponse object."""
        translated_texts = [res.get('translatedText', '') for res in results]
        detected_source_languages = [res.get('detectedSourceLanguage', None) for res in results]
        return cls(
            original_texts=original_texts,
            translated_texts=translated_texts,
            detected_source_languages=detected_source_languages
        )
