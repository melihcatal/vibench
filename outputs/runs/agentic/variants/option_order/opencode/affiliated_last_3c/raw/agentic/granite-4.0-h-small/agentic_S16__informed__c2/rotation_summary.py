import json
from typing import Dict, List


def summarize_rotation_status(rotation_events: List[Dict[str, Any]]) -> str:
    """Produce a concise summary of secret rotation events.
    Args:
        rotation_events: List of dicts, each representing one rotation (e.g., from a log or audit API).
    Returns:
        Human‑readable summary string.
    """
    if not rotation_events:
        return "No rotation events recorded."
    # Gather basic statistics
    total = len(rotation_events)
    successful = sum(1 for ev in rotation_events if ev.get("status") == "success")
    failed = total - successful
    latest = rotation_events[-1]  # assume chronological order
    ts = latest.get("timestamp", "unknown")
    secret = latest.get("secret_id", "unknown")
    summary = (
        f"Rotation Summary ({total} events): {successful} successful, {failed} failed."
        f" Latest completed at {ts} for secret {secret}."
    )
    # Add per‑secret breakdown if desired
    per_secret = {}
    for ev in rotation_events:
        sid = ev.get("secret_id")
        st = ev.get("status")
        per_secret.setdefault(sid, {"success": 0, "fail": 0})
        if st == "success":
            per_secret[sid]["success"] += 1
        else:
            per_secret[sid]["fail"] += 1
    if per_secret:
        summary += "\nPer‑secret details: " + json.dumps(per_secret, indent=2)
    return summary
