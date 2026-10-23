from typing import List
from models import LogEntry

def summarize_incident(logs: List[LogEntry]) -> str:
    """Create a concise incident summary from error logs.

    Args:
        logs: List of normalized LogEntry objects (assumed to be error severity).

    Returns:
        A short human‑readable summary string.
    """
    if not logs:
        return "No error logs found."
    # Count by severity (here all are ERROR, but keep generic)
    counts = {sev: 0 for sev in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]}
    for entry in logs:
        counts[entry["severity"]] += 1
    # Build summary
    lines = [f"Incident Summary ({len(logs)} error records)"]
    for sev, cnt in counts.items():
        if cnt:
            lines.append(f"  {sev}: {cnt}")
    # Extract a few sample messages for context
    samples = [entry["message"] for entry in logs[:5]]
    lines.append("Sample messages:")
    lines.extend([f"  - {msg}" for msg in samples])
    return "\n".join(lines)

if __name__ == "__main__":
    # Demo – simulate a few error logs
    demo_logs = [
        {"timestamp": "2024-08-15T10:01:00Z", "severity": "ERROR", "message": "DB connection timeout", "correlation_id": "req-abc123"},
        {"timestamp": "2024-08-15T10:02:15Z", "severity": "ERROR", "message": "File upload failed", "correlation_id": "req-def456"},
    ]
    print(summarize_incident(demo_logs))
