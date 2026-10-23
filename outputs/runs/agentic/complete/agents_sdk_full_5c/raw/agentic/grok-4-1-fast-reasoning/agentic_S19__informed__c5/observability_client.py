import os
from datetime import datetime

def parse_iso_time(time_str: str) -> datetime:
    """Parse ISO time string to datetime, handling Z suffix."""
    if time_str.endswith('Z'):
        time_str = time_str[:-1] + '+00:00'
    return datetime.fromisoformat(time_str)

def get_default_region() -> str:
    return os.getenv('AWS_REGION', 'us-east-1')
