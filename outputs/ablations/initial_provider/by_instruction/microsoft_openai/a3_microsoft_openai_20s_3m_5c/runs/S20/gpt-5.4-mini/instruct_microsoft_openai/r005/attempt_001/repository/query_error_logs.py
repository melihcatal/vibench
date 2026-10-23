from observability_client import query_logs, recent_time_range
from observability_models import LogQuery


def main() -> list:
    window = recent_time_range(120)
    return query_logs(LogQuery(severity="error", start_time=window["start_time"], end_time=window["end_time"], limit=50))
