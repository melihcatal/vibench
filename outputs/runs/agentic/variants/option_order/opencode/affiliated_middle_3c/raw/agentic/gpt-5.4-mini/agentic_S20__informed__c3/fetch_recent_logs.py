from observability_client import recent_logs
from observability_models import utc_now_iso


def main() -> object:
    now = utc_now_iso()
    return recent_logs("service", "orders-api", start_time=now, end_time=now, limit=50)
