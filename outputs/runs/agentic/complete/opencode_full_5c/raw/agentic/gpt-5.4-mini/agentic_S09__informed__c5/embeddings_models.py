from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence


def normalize_vector(values: Sequence[float]) -> List[float]:
    vector = [float(v) for v in values]
    norm = sum(v * v for v in vector) ** 0.5
    return [v / norm for v in vector] if norm else vector


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    l = [float(v) for v in left]
    r = [float(v) for v in right]
    size = min(len(l), len(r))
    if not size:
        return 0.0
    dot = sum(l[i] * r[i] for i in range(size))
    ln = sum(v * v for v in l) ** 0.5
    rn = sum(v * v for v in r) ** 0.5
    return dot / (ln * rn) if ln and rn else 0.0


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str


def extract_embeddings(response: Any) -> List[List[float]]:
    if hasattr(response, "embeddings"):
        return [
            list(item.values) if hasattr(item, "values") else list(item)
            for item in response.embeddings
        ]
    if isinstance(response, dict):
        items = response.get("embeddings") or response.get("data") or []
        result = []
        for item in items:
            if isinstance(item, dict) and "embedding" in item:
                result.append(list(item["embedding"]))
            elif isinstance(item, dict) and "values" in item:
                result.append(list(item["values"]))
        return result
    return []
