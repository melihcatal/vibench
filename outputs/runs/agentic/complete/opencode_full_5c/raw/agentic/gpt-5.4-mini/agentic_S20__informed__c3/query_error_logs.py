from datetime import timedelta

from observability_client import load_config, now_utc, query_logs
from observability_models import build_severity_query


def main() -> dict:
    cfg = load_config()
    end = now_utc()
    start = end - timedelta(hours=2)
    query = build_severity_query("error", cfg.service, "status:500")
    return query_logs(query, start, end, cfg, limit=25)
