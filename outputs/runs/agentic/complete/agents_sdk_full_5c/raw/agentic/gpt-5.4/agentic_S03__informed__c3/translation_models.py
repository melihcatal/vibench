from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "EN"
    preserve_formatting: bool = True
    tag_handling: Optional[str] = None
    formality: Optional[str] = None
    glossary_id: Optional[str] = None
    context: Optional[str] = None
    model_type: Optional[str] = None

    def to_deepl_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": self.text,
            "target_lang": self.target_language,
            "preserve_formatting": self.preserve_formatting,
        }
        if self.source_language:
            payload["source_lang"] = self.source_language
        if self.tag_handling:
            payload["tag_handling"] = self.tag_handling
        if self.formality:
            payload["formality"] = self.formality
        if self.glossary_id:
            payload["glossary"] = self.glossary_id
        if self.context:
            payload["context"] = self.context
        if self.model_type:
            payload["model_type"] = self.model_type
        return payload


@dataclass(slots=True)
class TranslationResponse:
    text: str
    detected_source_language: Optional[str] = None
    billed_characters: Optional[int] = None
    provider: str = "DeepL"
    raw: Any = None


@dataclass(slots=True)
class BatchTranslationResponse:
    translations: List[TranslationResponse] = field(default_factory=list)
    provider: str = "DeepL"



def normalize_texts(texts: Sequence[str]) -> List[str]:
    normalized = [str(text) for text in texts]
    if not normalized:
        raise ValueError("texts must not be empty")
    return normalized



def normalize_mapping_values(data: Mapping[str, Any]) -> Dict[str, str]:
    if not data:
        raise ValueError("data must not be empty")
    return {str(key): str(value) for key, value in data.items()}
