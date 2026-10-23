from typing import Dict, Any, List
from datetime import datetime

LogEvent = Dict[str, Any]


def parse_time_range(start_iso: str, end_iso: str) -> tuple[int, int]:
    start = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
    return int(start.timestamp()), int(end.timestamp())
