from typing import List


def embedding_job_summary(results: List[dict]) -> str:
    """Summarise a list of embedding job result dicts.

    Expected each dict to contain at least 'doc_id' and 'similarity' fields.
    Returns a concise markdown summary.
    """
    if not results:
        return "No embedding results to summarise."
    lines = ["## Embedding Job Summary"]
    for r in results:
        lines.append(
            f"- Document **{r.get('doc_id', 'unknown')}**: similarity {r.get('similarity'):.4f}"
        )
    return "\\n".join(lines)
