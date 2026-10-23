import os
from datetime import datetime, timezone
from typing import Dict, Tuple

DD_SITE = os.getenv("DD_SITE", "datadoghq.com")


def current_time_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def time_range_ms(hours_back: int = 1) -> Tuple[int, int]:
    now_ms = current_time_ms()
    start_ms = now_ms - (hours_back * 3600 * 1000)
    return start_ms, now_ms


def build_datadog_headers(api_key: str, app_key: str) -> Dict[str, str]:
    return {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }
