def summarize_embedding_job(result: list[float]) -> str:
    """Generate a brief summary for an embedding job result.
    Example: indicate dimensionality, range, or any notable properties.
    """
    if not result:
        return "No embedding returned."
    dim = len(result)
    min_val = min(result)
    max_val = max(result)
    return f"Embedding of dimension {dim} with values ranging from {min_val:.4f} to {max_val:.4f}."
