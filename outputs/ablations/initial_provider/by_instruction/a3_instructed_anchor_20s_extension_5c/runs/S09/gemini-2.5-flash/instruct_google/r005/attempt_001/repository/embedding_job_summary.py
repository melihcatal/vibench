def summarize_embedding_job(embeddings: list[list[float]], job_id: str = "") -> dict:
    """Summarizes the results of an embedding job.

    Args:
        embeddings: A list of embedding vectors generated during the job.
        job_id: An optional identifier for the embedding job.

    Returns:
        A dictionary containing summary information.
    """
    num_embeddings = len(embeddings)
    embedding_dimension = len(embeddings[0]) if embeddings else 0

    summary = {
        "job_id": job_id,
        "status": "completed",
        "total_embeddings_generated": num_embeddings,
        "embedding_dimension": embedding_dimension,
        "message": f"Successfully generated {num_embeddings} embeddings with dimension {embedding_dimension}."
    }
    return summary
