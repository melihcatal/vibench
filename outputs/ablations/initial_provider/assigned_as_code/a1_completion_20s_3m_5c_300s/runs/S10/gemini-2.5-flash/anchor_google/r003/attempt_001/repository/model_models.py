from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class TextPayload:
    text: str

@dataclass
class SummaryResponse:
    text: str

@dataclass
class JsonResponse:
    json_data: Dict[str, Any]

@dataclass
class AnswerResponse:
    answer: str

@dataclass
class ContentBlock:
    text: str

@dataclass
class EmbeddingResponse:
    embedding: List[float]
