# [HELPER] observability_models.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

class MetricQueryRequest:
    def __init__(self, metric: str, filter: str = '', start_time: str = '', end_time: str = '',
                 aggregation: str = 'Average', interval: str = 'PT1M', resource_id: str = ''):
        self.metric = metric
        self.filter = filter
        self.start_time = start_time
        self.end_time = end_time
        self.aggregation = aggregation
        self.interval = interval
        self.resource_id = resource_id

class MetricDataPoint:
    def __init__(self, timestamp: datetime, value: float, *args, **kwargs):
        self.timestamp = timestamp
        self.value = value
        self.tags = kwargs

class MetricQueryResponse:
    def __init__(self, timeseries: List[Dict[str, Any]]):
        # Azure Monitor returns a list of 'timeseries' objects with 'data' list
        self.timeseries = timeseries
        self.flat_points = []
        self._flatten()

    def _flatten(self):
        for ts in self.timeseries:
            for pt in ts.get('data', []):
                self.flat_points.append(MetricDataPoint(timestamp=datetime.fromisoformat(pt['timeStamp']),
                                                         value=pt['total']))

    def to_dataframe(self):
        """Optional helper to convert to pandas DataFrame (requires pandas)."""
        import pandas as pd
        df = pd.DataFrame([p.__dict__ for p in self.flat_points])
        return df