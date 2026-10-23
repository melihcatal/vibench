def generate_audio_brief(
    retrieved_results: list[tuple[str, float]], max_length: int = 200
) -> str:
    """Create a spoken brief from retrieved search results.

    Args:
        retrieved_results: List of (document_text, similarity_score) tuples from a search.
        max_length: Approximate character limit for the brief (to keep it concise for audio).

    Returns:
        A plain‑text English brief that summarizes the most relevant results.
    """
    # Keep only the highest‑scoring documents up to max_length characters
    brief_parts = ["Retrieved results for your query:"]
    chars_used = len(brief_parts[0])
    for i, (doc, score) in enumerate(retrieved_results, start=1):
        snippet = f"  {i}. {doc[:80]}... (score: {score:.3f})"
        if chars_used + len(snippet) < max_length:
            brief_parts.append(snippet)
            chars_used += len(snippet) + 1  # add one for newline
        else:
            break
    # Join and trim if we exceeded the limit
    return "\n".join(brief_parts)
