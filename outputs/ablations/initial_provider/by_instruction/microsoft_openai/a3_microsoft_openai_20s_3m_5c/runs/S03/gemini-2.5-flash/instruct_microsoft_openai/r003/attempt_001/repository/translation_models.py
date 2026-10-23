import dataclasses

@dataclasses.dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class TranslationResponse:
    translated_text: str
