def summarize_embedding_job(results: dict) -> str:
    """Create a brief textual summary of an embedding job result.
    Expected input format: {\"num_texts\": int, \"embeddings\": List[dict]}.
    """
    num_texts = results.get('num_texts', 0)
    embeddings = results.get('embeddings', [])
    summary = f'Embedding job processed {num_texts} texts.'
    if embeddings:
        summary += f' First embedding model: {embeddings[0].get('model', 'N/A')}'.
    return summary
