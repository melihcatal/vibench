import json
from datetime import datetime

# This module is designed to work with embedding job results,
# potentially originating from Google Cloud Vertex AI Embeddings.
# The summary functions are generic but keep in mind the context of the provider.

def summarize_embedding_job_results(job_results: list) -> dict:
    """
    Summarizes the results of an embedding job.

    Args:
        job_results: A list of dictionaries, where each dictionary represents
                     the result of embedding a single text, e.g.,
                     {"text": "...", "embedding": [...], "status": "success/failure", "time_taken": N}

    Returns:
        A dictionary containing the summary statistics of the embedding job.
    """
    total_texts = len(job_results)
    successful_embeddings = sum(1 for r in job_results if r.get("status") == "success")
    failed_embeddings = total_texts - successful_embeddings
    
    total_time_taken = sum(r.get("time_taken", 0) for r in job_results if r.get("time_taken") is not None)
    
    summary = {
        "total_texts_processed": total_texts,
        "successful_embeddings": successful_embeddings,
        "failed_embeddings": failed_embeddings,
        "total_processing_time_seconds": total_time_taken,
        "average_time_per_text_seconds": total_time_taken / total_texts if total_texts > 0 else 0,
        "summary_generated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    return summary
