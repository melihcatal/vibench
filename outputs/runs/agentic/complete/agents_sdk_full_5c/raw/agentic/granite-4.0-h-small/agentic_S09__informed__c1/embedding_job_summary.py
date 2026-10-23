import json

def summarize_embedding_job(results: list[tuple[str, float]]) -> str:
    """Create a human‑readable summary of an embedding‑search job.",
    summary_lines = ["Embedding Search Results:"]
    for idx, score in results[:5]:  # top 5 hits
        summary_lines.append(f"  {idx}: {score:.4f}")
    summary_lines.append(f"Total hits: {len(results)}")
    return "\n".join(summary_lines)


def write_summary_to_file(results: list[tuple[str, float]], filepath: str = "embedding_summary.txt") -> None:
    content = summarize_embedding_job(results)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Summary written to {filepath}")