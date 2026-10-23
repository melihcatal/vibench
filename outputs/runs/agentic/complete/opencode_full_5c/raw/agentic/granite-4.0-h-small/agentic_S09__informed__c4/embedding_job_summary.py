from typing import List

# Example summary format (can be extended as needed)


def summarize_embedding_job(results: List[dict]) -> str:
    """Summarize embedding job results.

    Args:
        results (List[dict]): List of result dicts from embeddings.
    Returns:
        str: Summary string.
    """
    summary_lines = ["Embedding Job Summary:"]
    for idx, result in enumerate(results, start=1):
        summary_lines.append(f"Result {idx}: embedding = {result['embedding'][:5]}...")
    return "\\n".join(summary_lines)
