import json
from pathlib import Path
from observability_client import get_log_client
from observability_models import LogEvent, QueryFilters


def incident_summary(error_logs_path: Path, output_path: Path):
    """Summarize error‑log findings for incident review.

    1. Reads a JSON file produced by `query_error_logs` (or any JSON array of LogEvent dicts).
    2. Extracts per‑error‑type counts, top sources, and recent timestamps.
    3. Writes a concise markdown summary to `output_path`.
    """
    data = json.loads(error_logs_path.read_text())
    # Cast entries to LogEvent for convenience
    events = [LogEvent(**entry) for entry in data]

    # --- High‑level stats ---
    total = len(events)
    if total == 0:
        summary = "No error logs found."
    else:
        # Count by severity / error code (if present)
        counts = {}
        sources = {}
        recent = max(e.timestamp for e in events)
        for ev in events:
            typ = ev.level
            counts[typ] = counts.get(typ, 0) + 1
            src = ev.get("source", "unknown")
            sources[src] = sources.get(src, 0) + 1
        # Top 3 error types
        top_errors = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
        # Top 3 affected sources
        top_sources = sorted(sources.items(), key=lambda kv: kv[1], reverse=True)[:3]
        summary = (
            f"# Incident Summary (last 60 min)`\n"
            f"| Metric | Value |\n|---|---|\n"
            f"| Total Errors | {total} |\n"
            f"| Most Recent Timestamp | {recent} |\n"
        )
        summary += "\n**Top Error Types**\n"
        for typ, cnt in top_errors:
            summary += f"| {typ} | {cnt} |\n"
        summary += "\n**Top Affected Sources**\n"
        for src, cnt in top_sources:
            summary += f"| {src} | {cnt} |\n"
    output_path.write_text(summary)
