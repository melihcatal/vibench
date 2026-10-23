from typing import List, Dict, Any
from dataclasses import dataclass

# These are local, provider-agnostic data structures.
# They can be used for internal representation before converting
# to a provider-specific format.

@dataclass
class SummarizeRequest:
    text: str
    model: str = "default"

@dataclass
class SummarizeResponse:
    summary: str

@dataclass
class ExtractRequest:
    text: str
    schema: Dict[str, Any]

@dataclass
class ExtractResponse:
    data: Dict[str, Any]

@dataclass
class QA_Request:
    question: str
    context: str

@dataclass
class QA_Response:
    answer: str

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
