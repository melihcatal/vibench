from typing import List, Dict
import datetime

def summarize_embedding_job_results(
    job_id: str, 
    embeddings_data: List[Dict[str, List[float]]],
    provider_source: str = "Google AI Gemini Embedding",
) -> Dict[str, str]:
    """
    Summarizes the results of an embedding job.
    Assumes embeddings_data contains a list of dictionaries, each with an 'embedding' key
    containing a list of floats, originating from a specified provider like Google AI.
    """
    total_embeddings = len(embeddings_data)
    if total_embeddings == 0:
        return {
            "job_id": job_id,
            "status": "completed",
            "summary": f"No embeddings generated from {provider_source}.",
            "timestamp": datetime.datetime.now().isoformat()
        }

    embedding_dimension = len(embeddings_data[0]["embedding"]) if embeddings_data and embeddings_data[0]["embedding"] else 0
    
    summary_text = (
        f"Embedding job '{job_id}' completed successfully using {provider_source}. "
        f"Total embeddings generated: {total_embeddings}. "
        f"Each embedding has a dimension of {embedding_dimension}."
    )

    return {
        "job_id": job_id,
        "status": "completed",
        "summary": summary_text,
        "timestamp": datetime.datetime.now().isoformat()
    }
