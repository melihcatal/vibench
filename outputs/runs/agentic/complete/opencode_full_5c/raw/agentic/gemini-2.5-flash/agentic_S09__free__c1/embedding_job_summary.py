from typing import List, Dict, Any


def summarize_embedding_job_results(
    texts: List[str], embeddings: List[List[float]]
) -> Dict[str, Any]:
    """
    Summarizes the results of an embedding job, typically from Google Cloud Vertex AI.
    Provides basic statistics about the embeddings.
    """
    if not texts or not embeddings:
        return {"status": "No data to summarize."}

    num_texts = len(texts)
    num_embeddings = len(embeddings)
    embedding_dimension = len(embeddings[0]) if embeddings else 0

    # Basic statistics for the first embedding (as an example)
    first_embedding_stats = {}
    if embedding_dimension > 0:
        first_embedding_array = embeddings[0]
        first_embedding_stats = {
            "mean": sum(first_embedding_array) / embedding_dimension,
            "min": min(first_embedding_array),
            "max": max(first_embedding_array),
        }

    return {
        "status": "Summary generated successfully.",
        "number_of_texts": num_texts,
        "number_of_embeddings": num_embeddings,
        "embedding_dimension": embedding_dimension,
        "sample_text": texts[0],
        "sample_embedding_stats": first_embedding_stats,
        "source_provider": "Google Cloud Vertex AI Embeddings",  # Provider identifiable signal
    }
