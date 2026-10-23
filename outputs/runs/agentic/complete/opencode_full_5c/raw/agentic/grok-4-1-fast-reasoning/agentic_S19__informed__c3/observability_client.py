from datetime import datetime, timedelta
import os
from typing import Tuple


def get_time_window(window_minutes: int = 60) -> Tuple[datetime, datetime]:
    end = datetime.utcnow()
    start = end - timedelta(minutes=window_minutes)
    return start, end


def get_aws_region() -> str:
    return os.getenv("AWS_REGION", "us-east-1")
