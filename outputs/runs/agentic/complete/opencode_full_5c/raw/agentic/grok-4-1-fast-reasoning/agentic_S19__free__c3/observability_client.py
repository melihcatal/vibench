import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta


def get_aws_region() -> str:
    return os.getenv("AWS_REGION", "us-east-1")


def make_dimensions(dim_list: Optional[List[Dict[str, str]]]) -> List[Dict[str, str]]:
    if not dim_list:
        return []
    return [{"Name": d["name"], "Value": d["value"]} for d in dim_list]


def create_recent_window(duration_minutes: int) -> Dict[str, datetime]:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)
    return {"start": start_time, "end": end_time}
