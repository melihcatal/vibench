# [LATER-STEP] embedding_job_summary.py
# Summarize results from an embedding job (query + document similarities)

from typing import Dict
from embeddings_client import get_openai_client


SUMMARY_TEMPLATE = """
Embedding Job Summary\n---------------------\nQuery: {query}\nNumber of documents processed: {doc_count}\nTop similar documents (by score):\n{top_items}\n"""


def create_summary(results: Dict[str, float], query: str, top_n: int = 5) -> str:
    """Generate a human‑readable summary of embedding search results.

    Args:\n        results: Mapping of document text to its similarity score.\n        query: The original query string.\n        top_n: How many top matches to list.\n
    Returns:\n        A formatted summary string.\n    """
    # Sort by descending score and keep top_n entries
    top_items = sorted(
        [(doc, score) for doc, score in results.items()],
        key=lambda x: x[1],
        reverse=True,
    )[:top_n]

    doc_count = len(results)
    formatted_items = \"\n\n\".join(f"Score: {score:.4f} – {doc}" for doc, score in top_items)

    return SUMMARY_TEMPLATE.format(
        query=query,
        doc_count=doc_count,
        top_items=formatted_items if formatted_items else "No documents retrieved.",
    )

# Example usage (uncomment to test)\n# if __name__ == "__main__":
#     sample = {\"Doc A\": 0.92, \"Doc B\": 0.87, \"Doc C\": 0.80}\n#     print(create_summary(sample, \"example query\"))
