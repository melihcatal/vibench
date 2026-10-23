from typing import List, Dict
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import LogHit, normalize_logs

# Helper to decide if a log line is critical (e.g., contains keywords)

def _is_critical(message: str) -> bool:
    lower = message.lower()
    return any(token in lower for token in ["exception", "failure", "error", "fatal"])


def incident_summary(log_hits: List[LogHit], window_hours: int = 6) -> Dict[str, any]:
    """Create a concise incident report from recent error logs.

    Args:
        log_hits (List[LogHit]): List of error logs from a query.
        window_hours (int): How far back in hours to consider.
    Returns:
        Dict[str, any]: Summary with timestamp, total count, critical count, and sample messages.
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=window_hours)
    recent_hits = [h for h in log_hits if datetime.fromisoformat(h["timestamp"].replace("Z", "+00:00")) >= cutoff]
    total = len(recent_hits)
    critical = sum(1 for h in recent_hits if _is_critical(h["message"]))
    # Sample 5 critical messages
    samples = [h["message"] for h in recent_hits if _is_critical(h["message"])][:5]
    return {
        "timestamp": now.isoformat() + "Z",
        "total_error_logs": total,
        "critical_logs": critical,
        "sample_critical_messages": samples
    }