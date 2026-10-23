from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple
from observability_models import MetricDatapoint

def get_recent_time_window(duration_minutes: int = 60) -> Tuple[datetime, datetime]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=duration_minutes)
    return start_time, end_time

def normalize_cloudwatch_datapoints(raw_datapoints: List[Dict]) -> List[MetricDatapoint]:
    datapoints = []
    for raw in raw_datapoints:
        dp = MetricDatapoint(
            timestamp=raw['Timestamp'],
            average=raw.get('Average'),
            minimum=raw.get('Minimum'),
            maximum=raw.get('Maximum'),
            sample_count=raw.get('SampleCount'),
            sum_=raw.get('Sum'),
            unit=raw.get('Unit'),
        )
        datapoints.append(dp)
    return datapoints