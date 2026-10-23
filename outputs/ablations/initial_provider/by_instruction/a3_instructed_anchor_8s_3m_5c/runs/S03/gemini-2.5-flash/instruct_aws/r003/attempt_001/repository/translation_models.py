from dataclasses import dataclass

@dataclass
class TranslationRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclass
class TranslationResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str
