from dataclasses import dataclass
from typing import Optional
from google.cloud import translate_v3 as translate
from translation_client import get_glossary_config

@dataclass
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str
    model: str = "google-translate-v3"
    glossary_id: Optional[str] = None

    @property
    def glossary_config(self) -> Optional[translate.TranslateTextGlossaryConfig]:
        return get_glossary_config(self.glossary_id)

@dataclass
class TranslationResponse:
    translated_text: str

    @classmethod
    def from_google_response(cls, response: translate.TranslateTextResponse) -> "TranslationResponse":
        return cls(translated_text=response.translations[0].translated_text)