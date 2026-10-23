from math import isnan
from datetime import datetime
from typing import List, Any, Tuple, Dict
from observability_models import TimeWindow, MetricDatapoint


def parse_time_window(window: TimeWindow) -> Tuple[datetime, datetime]:
    z_replace = lambda s: s[:-1] + "+00:00" if s.endswith("Z") else s
    start = datetime.fromisoformat(z_replace(window.start))
    end = datetime.fromisoformat(z_replace(window.end))
    return start, end


def normalize_get_metric_data(result: Dict[str, Any]) -> List[MetricDatapoint]:
    timestamps: List[datetime] = result["Timestamps"]
    values: List[float] = result["Values"]
    return [
        MetricDatapoint(timestamp=timestamps[i].isoformat() + "Z", value=values[i])
        for i in range(len(timestamps))
        if not isnan(values[i])
    ]
