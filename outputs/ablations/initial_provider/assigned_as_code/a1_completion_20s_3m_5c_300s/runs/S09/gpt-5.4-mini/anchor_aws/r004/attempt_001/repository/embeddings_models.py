import json
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence


def normalize_text(value: Any) -> str:
    return str(value).strip()


def normalize_texts(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [normalize_text(value)]
    return [normalize_text(item) for item in value]


def parse_embedding_response(response: Dict[str, Any]) -> List[float]:
    if "embedding" in response:
        return list(response["embedding"])
    if "embeddings" in response and response["embeddings"]:
        first = response["embeddings"][0]
        return list(first["embedding"] if isinstance(first, dict) and "embedding" in first else first)
    return []


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or not right:
        return 0.0
    size = min(len(left), len(right))
    dot = sum(float(left[i]) * float(right[i]) for i in range(size))
    left_norm = sum(float(left[i]) ** 2 for i in range(size)) ** 0.5
    right_norm = sum(float(right[i]) ** 2 for i in range(size)) ** 0.5
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


@dataclass
class EmbeddingRequest:
    text: str

    def to_payload(self) -> Dict[str, Any]:
        return {"text": normalize_text(self.text)}


@dataclass
class BatchEmbeddingRequest:
    texts: List[str]

    def to_payload(self) -> Dict[str, Any]:
        return {"texts": normalize_texts(self.texts)}


def parse_json_body(body: Any) -> Dict[str, Any]:
    if isinstance(body, (bytes, bytearray)):
        return json.loads(body.decode("utf-8"))
    if hasattr(body, "read"):
        return json.loads(body.read())
    if isinstance(body, str):
        return json.loads(body)
    return dict(body)
