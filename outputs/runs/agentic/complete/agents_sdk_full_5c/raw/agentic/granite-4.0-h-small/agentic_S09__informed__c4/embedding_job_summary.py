# embedding_job_summary.py

def embedding_job_summary(results: list[dict]) -> str:
    """Summarize a list of embedding operation results.

    Args:
        results (List[Dict]): Each dict contains provider-specific response fields.

    Returns:
        str: Human‑readable summary including count, success rate, and example identifiers.
    """
    total = len(results)
    successes = sum(1 for r in results if r.get("status") == "completed")
    failed = total - successes
    summary = f"Embedding job summary: {total} requests submitted.\n"
    if successes:
        summary += f"  Successes: {successes} (e.g., ID {results[0].get('request_id')})\n"
    if failed:
        summary += f"  Failures: {failed} (e.g., ID {results[failed-1].get('request_id')})\n"
    return summary
