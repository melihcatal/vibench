from typing import List, Dict, Optional
from pydantic import BaseModel


class EmbeddingJobResult(BaseModel):
    document_id: str
    embedding: List[float]
    status: str
    error: Optional[str] = None


class EmbeddingJobSummary(BaseModel):
    total_documents: int
    successful_documents: int
    failed_documents: int
    average_embedding_length: float
    results: List[EmbeddingJobResult]


def summarize_embedding_job(results: List[EmbeddingJobResult]) -> EmbeddingJobSummary:
    """
    Summarizes the results of an embedding job.

    Args:
        results: List of embedding job results.

    Returns:
        Summary of the embedding job, including success/failure counts and average embedding length.
    """
    total_documents = len(results)
    successful_documents = sum(1 for result in results if result.status == "success")
    failed_documents = total_documents - successful_documents

    if successful_documents > 0:
        average_embedding_length = (
            sum(
                len(result.embedding)
                for result in results
                if result.status == "success"
            )
            / successful_documents
        )
    else:
        average_embedding_length = 0.0

    return EmbeddingJobSummary(
        total_documents=total_documents,
        successful_documents=successful_documents,
        failed_documents=failed_documents,
        average_embedding_length=average_embedding_length,
        results=results,
    )
