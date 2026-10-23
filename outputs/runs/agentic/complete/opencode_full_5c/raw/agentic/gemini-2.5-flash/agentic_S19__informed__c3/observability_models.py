import datetime
from typing import Dict, Any, List


class MetricQuery:
    """Represents a query for Google Cloud Monitoring metrics."""

    def __init__(
        self,
        project_id: str,
        metric_type: str,
        end_time: datetime.datetime,
        start_time: datetime.datetime,
        interval_minutes: int = 5,
        filters: List[str] = None,
        aggregation_function: str = None,
    ):
        self.project_id = project_id
        self.metric_type = metric_type
        self.end_time = end_time
        self.start_time = start_time
        self.interval_minutes = interval_minutes
        self.filters = filters if filters is not None else []
        self.aggregation_function = aggregation_function


class MetricResult:
    """Represents the result of a Google Cloud Monitoring metric query."""

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def to_dict(self):
        return {"data": self.data}

    @staticmethod
    def from_response(response: Any) -> "MetricResult":
        # Basic normalization for Google Cloud Monitoring TimeSeries response
        points = []
        for series in response.time_series:
            for point in series.points:
                points.append(
                    {
                        "value": point.value.double_value
                        if point.value.WhichOneof("value_type") == "double_value"
                        else point.value.int64_value,
                        "timestamp": point.interval.end_time.isoformat(),
                    }
                )
        return MetricResult(data=points)
