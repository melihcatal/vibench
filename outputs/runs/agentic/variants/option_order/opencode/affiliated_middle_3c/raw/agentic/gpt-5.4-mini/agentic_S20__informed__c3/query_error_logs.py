from observability_client import search_logs
from observability_models import LogQuery, utc_now_iso


def main() -> object:
    return search_logs(
        LogQuery(
            query="service:orders-api status:error",
            start_time=utc_now_iso(),
            end_time=utc_now_iso(),
            severity="ERROR",
            limit=25,
        )
    )
