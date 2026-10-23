from typing import Dict, Any, List


class MetricQuery:
    def __init__(
        self,
        project_id: str,
        metric_type: str,
        interval_start_time: str,
        interval_end_time: str,
        aligner: str = monitoring_v3.TimeSeriesAligner.ALIGN_MEAN.name,
        reducer: str = monitoring_v3.TimeSeriesReducer.REDUCE_MEAN.name,
        period: str = '60s',
        filters: List[str] = None,
    ):
        self.project_id = project_id
        self.metric_type = metric_type
        self.interval_start_time = interval_start_time
        self.interval_end_time = interval_end_time
        self.aligner = aligner
        self.reducer = reducer
        self.period = period
        self.filters = filters if filters is not None else []


class MetricDatapoint:
    def __init__(self, timestamp: str, value: Any, labels: Dict[str, str]):
        self.timestamp = timestamp
        self.value = value
        self.labels = labels


class MetricQueryResult:
    def __init__(self, metric_name: str, datapoints: List[MetricDatapoint]):
        self.metric_name = metric_name
        self.datapoints = datapoints
