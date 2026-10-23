from datetime import timedelta

from observability_client import load_config, now_utc, query_logs
from observability_models import build_field_query


def main() -> dict:
    cfg = load_config()
    end = now_utc()
    start = end - timedelta(minutes=30)
    query = build_field_query("env", "production", cfg.service)
    return query_logs(query, start, end, cfg, limit=50)
