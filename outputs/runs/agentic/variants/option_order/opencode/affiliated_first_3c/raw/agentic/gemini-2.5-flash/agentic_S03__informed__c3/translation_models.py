from typing import Dict, List, Optional, Any


class TranslationRequest:
    def __init__(
        self,
        text: Any,
        target_language: str,
        source_language: Optional[str] = None,
        format: Optional[str] = None,
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language
        self.format = format


class TranslationResponse:
    def __init__(
        self, translated_text: Any, detected_source_language: Optional[str] = None
    ):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language
