import json
from log_embedding import embed_log_messages
from log_text_safety import safe_messages


def incident_summary(error_logs):
    """
    Summarize a collection of error logs for incident review.

    Parameters
    ----------
    error_logs: list[dict]
        List of log events previously retrieved from a log query.

    Returns
    -------
    dict
        Summary containing a short narrative, total count, and safe-embedded representation.
    """
    # Filter to only include safe message text (exclude unsafe content)
    safe = safe_messages(error_logs)
    # Generate a semantic embedding for the safe messages to enable quick similarity checks
    embeddings = embed_log_messages(safe)
    summary = {
        "total_errors": len(error_logs),
        "safe_sample": safe[:5],
        "embeddings": embeddings[:5],  # embed only first few for brevity
    }
    return summary
