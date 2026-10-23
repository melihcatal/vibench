from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    source_text: Any
    source_language: str
    target_language: str
    tone: Optional[str] = None

    def normalized_text(self) -> str:
        if isinstance(self.source_text, str):
            return self.source_text
        if self.source_text is None:
            return ""
        return str(self.source_text)

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "source_text": self.normalized_text(),
            "source_language": self.source_language,
            "target_language": self.target_language,
        }
        if self.tone:
            payload["tone"] = self.tone
        return payload


@dataclass
class TranslationResponse:
    translated_text: str
    provider: str
    model: str
    metadata: Dict[str, Any]

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_strings(items: Any) -> List[str]:
    if items is None:
        return []
    if isinstance(items, str):
        return [items]
    return ["" if item is None else str(item) for item in items]


def normalize_mapping_values(data: Dict[str, Any]) -> Dict[str, str]:
    return {key: "" if value is None else str(value) for key, value in data.items()}
