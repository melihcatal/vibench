# Later-step implementation
from datetime import datetime
from collections import Counter
from observability_client import get_logging_client
from observability_models import LogQueryParams, LogEvent, LogSearchResult

def summarize_error_logs(start_relative="30m"):
    """Summarize error‑log findings for incident review.

    Queries Loggly (example provider) for ERROR severity logs in the
    given time window, then aggregates by error code (if present) and
    produces a concise markdown summary.
    """
    client = get_logging_client()
    end = datetime.utcnow()
    start = end - parse_relative_duration(start_relative)
    query = f'severity:ERROR AND timestamp:[{int(start.timestamp()*1000)} TO {int(end.timestamp()*1000)}]'
    results = client.search_logs(query=query)
    # Normalize results to LogEvent objects
    events = [normalize_event(r) for r in results]
    code_counts = Counter(ev.metadata.get("error_code", "UNKNOWN") for ev in events)
    summary = [f"## Error‑log Summary ({start_relative} ago)\n"]
    summary.append(f"Total errors: {len(events)}\n")
    summary.append("### Top error codes\n")
    for code, cnt in code_counts.most_common(5):
        summary.append(f"- **{code}**: {cnt} occurrences\n")
    return "\n".join(summary)}