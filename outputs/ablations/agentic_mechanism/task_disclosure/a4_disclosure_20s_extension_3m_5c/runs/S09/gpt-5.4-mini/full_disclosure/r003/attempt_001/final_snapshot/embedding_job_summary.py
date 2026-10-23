import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence


@dataclass(frozen=True)
class EmbeddingJobSummary:
    provider: str
    model: str
    total_texts: int
    embedded_texts: int
    failed_texts: int
    dimensions: Optional[int]
    normalized: bool
    average_vector_norm: Optional[float]
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "total_texts": self.total_texts,
            "embedded_texts": self.embedded_texts,
            "failed_texts": self.failed_texts,
            "dimensions": self.dimensions,
            "normalized": self.normalized,
            "average_vector_norm": self.average_vector_norm,
            "notes": list(self.notes),
        }


def _vector_norm(values: Sequence[float]) -> float:
    return sum(float(value) * float(value) for value in values) ** 0.5


def summarize_embedding_job_results(
    response: Any,
    total_texts: Optional[int] = None,
    normalized: bool = False,
    dimensions: Optional[int] = None,
    provider: str = "openai",
) -> EmbeddingJobSummary:
    model = getattr(response, "model", "") or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    items = list(getattr(response, "data", []) or [])
    embedded_texts = len(items)
    resolved_total = total_texts if total_texts is not None else embedded_texts
    failed_texts = max(resolved_total - embedded_texts, 0)
    norms = [_vector_norm(getattr(item, "embedding", []) or []) for item in items]
    average_vector_norm = (sum(norms) / len(norms)) if norms else None
    notes: List[str] = []
    if failed_texts:
        notes.append(f"{failed_texts} texts did not produce embeddings")
    if normalized:
        notes.append("embeddings were normalized after retrieval")
    if dimensions is not None:
        notes.append(f"requested dimensions={dimensions}")
    return EmbeddingJobSummary(
        provider=provider,
        model=model,
        total_texts=resolved_total,
        embedded_texts=embedded_texts,
        failed_texts=failed_texts,
        dimensions=dimensions,
        normalized=normalized,
        average_vector_norm=average_vector_norm,
        notes=notes,
    )
