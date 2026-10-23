import time
from typing import Dict, Optional

def create_time_interval(window_minutes: int = 60) -> Dict:
    now = time.time()
    return {
        "start_time": {"seconds": int(now - window_minutes * 60)},
        "end_time": {"seconds": int(now)}
    }

def build_metric_filter(metric_name: str, dimensions: Optional[Dict[str, str]] = None) -> str:
    filter_str = f'metric.type = "{metric_name}"'
    if dimensions:
        for key, value in dimensions.items():
            filter_str += f' AND resource.labels["{key}"] = "{value}"'
    return filter_str
