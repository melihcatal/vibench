from typing import List, Dict, Any


def summarize_embedding_job_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarizes embedding job results.

    In a real scenario, this function would perform more complex aggregation,
    statistical analysis, or reporting on the embedding job outcomes.
    For this exercise, it simply returns a basic summary.
    """
    summary = {
        "total_embeddings_generated": len(results),
        "first_result_preview": results[0] if results else None,
        "status": "Summarized successfully",
    }
    print("Embedding job summary:", summary)
    return summary
