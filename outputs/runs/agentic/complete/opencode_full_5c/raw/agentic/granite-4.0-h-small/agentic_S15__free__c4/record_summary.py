# [LATER-STEP] record_summary.py
"""Utility to summarize a fetched document record.

Assumes the document contains a 'content' field (string) and 'metadata' (dict).
Generates a concise summary using a simple heuristic: first 2-3 sentences.
"""

from typing import Any, Dict


def summarize_record(document: Dict[str, Any]) -> str:
    """Return a short plain‑text summary of the document's content field.

    The summary contains at most the first three sentences of the 'content' field.
    If 'content' is missing or empty, returns an empty string.
    """
    content = document.get("content")
    if not content:
        return ""
    # Split on sentence delimiters (., !, ?) and rejoin the first three
    sentences = [s.strip() for s in content.split(".") if s.strip()]
    # Handle exclamation and question marks that may be attached to sentences
    sentences = [s.split("!")[0].split("?")[0].strip() for s in sentences]
    summary_sentences = sentences[:3]
    return " ".join(summary_sentences) + ("..." if len(sentences) > 3 else "")
