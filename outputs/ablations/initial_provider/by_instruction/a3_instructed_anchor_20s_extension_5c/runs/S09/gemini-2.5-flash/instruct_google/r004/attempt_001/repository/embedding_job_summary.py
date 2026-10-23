import os
from typing import List, Dict, Any
from google.cloud import logging

def summarize_embedding_job(job_id: str, results: List[Dict[str, Any]], status: str) -> Dict[str, Any]:
    """Summarizes embedding job results and logs them to Google Cloud Logging.

    Args:
        job_id: A unique identifier for the embedding job.
        results: A list of dictionaries, where each dictionary might contain 
                 'text' and 'embedding_vector_length' for example.
        status: The overall status of the embedding job (e.g., 'completed', 'failed').

    Returns:
        A dictionary summarizing the job.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = logging.Client(project=project_id)
    logger = client.logger("embedding_job_summaries")

    summary = {
        "job_id": job_id,
        "status": status,
        "total_texts_processed": len(results),
        "example_result": results[0] if results else None,
        "provider": "Google Cloud Vertex AI Embeddings (implied)"
    }

    logger.log_struct(summary, severity="INFO")

    return summary
