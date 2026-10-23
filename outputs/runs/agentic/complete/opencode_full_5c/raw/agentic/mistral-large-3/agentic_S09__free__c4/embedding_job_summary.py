from typing import List, Dict
from pydantic import BaseModel
import json


class EmbeddingJobResult(BaseModel):
    total_texts: int
    successful_embeddings: int
    failed_embeddings: int
    average_embedding_time_ms: float
    model_used: str


def embedding_job_summary(results: List[Dict]) -> str:
    total_texts = len(results)
    successful = sum(1 for r in results if r.get("success", False))
    failed = total_texts - successful
    avg_time = (
        sum(r.get("time_ms", 0) for r in results) / total_texts
        if total_texts > 0
        else 0
    )
    model = results[0].get("model", "unknown") if results else "unknown"

    summary = EmbeddingJobResult(
        total_texts=total_texts,
        successful_embeddings=successful,
        failed_embeddings=failed,
        average_embedding_time_ms=avg_time,
        model_used=model,
    )

    return summary.model_dump_json(indent=2)
