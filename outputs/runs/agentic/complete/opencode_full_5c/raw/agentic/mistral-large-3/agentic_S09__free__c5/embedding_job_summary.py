from typing import List, Dict, Optional
from pydantic import BaseModel
import numpy as np


class EmbeddingJobResult(BaseModel):
    document_id: str
    embedding: List[float]
    token_count: int
    success: bool
    error_message: Optional[str] = None


class EmbeddingJobSummary(BaseModel):
    total_documents: int
    successful_documents: int
    failed_documents: int
    total_tokens: int
    average_tokens_per_document: float
    results: List[EmbeddingJobResult]


def summarize_embedding_job(results: List[EmbeddingJobResult]) -> EmbeddingJobSummary:
    """Summarize the results of an embedding job."""
    total_documents = len(results)
    successful_documents = sum(1 for r in results if r.success)
    failed_documents = total_documents - successful_documents
    total_tokens = sum(r.token_count for r in results if r.success)
    average_tokens = (
        total_tokens / successful_documents if successful_documents > 0 else 0
    )

    return EmbeddingJobSummary(
        total_documents=total_documents,
        successful_documents=successful_documents,
        failed_documents=failed_documents,
        total_tokens=total_tokens,
        average_tokens_per_document=average_tokens,
        results=results,
    )
