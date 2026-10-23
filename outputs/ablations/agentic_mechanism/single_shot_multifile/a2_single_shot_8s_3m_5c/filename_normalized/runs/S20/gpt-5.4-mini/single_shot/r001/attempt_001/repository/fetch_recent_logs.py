from datetime import datetime, timedelta, timezone
import os

from observability_client import query_log_entries
from observability_models import LogQueryRequest, LogWindow, build_filter


if __name__ == "__main__":
    field_name = os.getenv("LOG_FIELD_NAME", "jsonPayload.service")
    field_value = os.getenv("LOG_FIELD_VALUE", "checkout-api")
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=int(os.getenv("LOOKBACK_MINUTES", "60")))
    query = LogQueryRequest(field_name=field_name, field_value=field_value, window=LogWindow(start_time=start_time, end_time=end_time), limit=int(os.getenv("LOG_LIMIT", "100")))
    filter_ = build_filter(query)
    entries = list(query_log_entries(filter_, page_size=query.limit))
    for entry in entries:
        print(getattr(entry, "payload", entry))
