from typing import NamedTuple

class TranslationRequest(NamedTuple):
    text: str
    source_language: str
    target_language: str

class TranslationResponse(NamedTuple):
    translated_text: str
