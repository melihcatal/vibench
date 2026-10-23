from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class TextResponse:
    text: str
    finish_reason: Optional[str] = None


@dataclass
class JsonResponse:
    json_data: Dict
    finish_reason: Optional[str] = None


@dataclass
class StreamedTextResponse:
    text_chunk: str


@dataclass
class SafetyRating:
    category: str
    probability: str


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    ratings: List[SafetyRating]
