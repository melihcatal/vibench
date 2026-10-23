from datetime import datetime, timedelta, timezone
import os

from observability_client import query_log_entries
from observability_models import LogQueryRequest, LogWindow, build_filter, summarize_entries


if __name__ == "__main__":
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=int(os.getenv("LOOKBACK_HOURS", "12")))
    query = LogQueryRequest(severity="ERROR", window=LogWindow(start_time=start_time, end_time=end_time), limit=500)
    entries = list(query_log_entries(build_filter(query), page_size=query.limit))
    summary = summarize_entries({"severity": getattr(e, "severity", None), "textPayload": getattr(e, "payload", None)} for e in entries)
    print({"total": summary.total, "by_severity": summary.by_severity, "messages": summary.messages[:20]})
