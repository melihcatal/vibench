import datetime
import json
from typing import List, Dict
from observability_models import LogEntry, normalize_log_entry
from observability_client import get_client
from log_text_safety import is_safe_text
from log_message_translate import translate_log_message
from log_embedding import embed_log_message

THRESHOLD_SEVERITY = {"error", "critical"}


def incident_summary(error_logs: List[dict], locale: str = "en") -> Dict[str, any]:
    """Summarize error-log findings for incident review.

    Args:
        error_logs: List of raw log dicts from query_error_logs.
        locale: Target locale for translated messages.
    Returns:
        Dictionary with counts, sample messages, safety flags, and embeddings.
    """
    summary = {
        "total": 0,
        "by_severity": {},
        "sample_safe_messages": [],
        "sample_unsafe_messages": [],
        "translated_samples": [],
        "embeddings": [],
        "recent_timestamp_range": {},
    }
    safe_messages = []
    unsafe_messages = []
    embeddings = []
    translated_samples = []

    for raw in error_logs:
        log = normalize_log_entry(raw)
        summary["total"] += 1
        sev = log.level
        summary["by_severity"][sev] = summary["by_severity"].get(sev, 0) + 1
        if sev in THRESHOLD_SEVERITY:
            msg = log.message
            if is_safe_text(msg):
                safe_messages.append(msg)
            else:
                unsafe_messages.append(msg)
            # Get embedding (embed first, may call external service)
            emb = embed_log_message(msg)
            embeddings.append(emb)
            # Translate for support view
            trans = translate_log_message(msg, target_locale=locale)
            translated_samples.append({"original": msg, "translated": trans})

    summary["sample_safe_messages"] = safe_messages[:5]
    summary["sample_unsafe_messages"] = unsafe_messages[:5]
    summary["translated_samples"] = translated_samples[:5]
    summary["embeddings"] = embeddings[:5]
    # Timestamp range of the batch
    timestamps = [normalize_log_entry(r).timestamp for r in error_logs]
    summary["recent_timestamp_range"] = {
        "earliest": min(timestamps),
        "latest": max(timestamps)
    }
    return summary
