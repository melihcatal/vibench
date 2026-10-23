from datetime import datetime, timedelta
from typing import Dict, Any, List
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest, MetricDatapoint
import datadog

def compare_metric_series(
    metric_name: str,
    start_time: str,
    end_time: str,
    filter_set_1: Dict[str, str],
    filter_set_2: Dict[str, str]
) -> Dict[str, List[MetricDatapoint]]:
    client = ObservabilityClient()

    # Convert ISO 8601 strings to timestamps
    start_timestamp = int(datetime.fromisoformat(start_time).timestamp())
    end_timestamp = int(datetime.fromisoformat(end_time).timestamp())

    def build_query(metric: str, dimensions: Dict[str, str]) -> str:
        tags = ",".join([f'{k}:{v}' for k, v in dimensions.items()])
        if tags:
            return f'{metric}{{tags:{tags}}}'
        return metric

    query_1 = build_query(metric_name, filter_set_1)
    query_2 = build_query(metric_name, filter_set_2)

    # Query for the first series
    response_1 = datadog.api.Metric.query(
        start=start_timestamp,
        end=end_timestamp,
        query=query_1
    )

    datapoints_1 = []
    if response_1 and response_1.get('series'):
        for series in response_1['series']:
            for point in series['pointlist']:
                # point is [timestamp_ms, value]
                timestamp_s = point[0] / 1000
                datapoints_1.append(MetricDatapoint(
                    timestamp=datetime.fromtimestamp(timestamp_s).isoformat(),
                    value=float(point[1]) if point[1] is not None else 0.0, # Handle None values
                    dimensions=filter_set_1
                ))

    # Query for the second series
    response_2 = datadog.api.Metric.query(
        start=start_timestamp,
        end=end_timestamp,
        query=query_2
    )

    datapoints_2 = []
    if response_2 and response_2.get('series'):
        for series in response_2['series']:
            for point in series['pointlist']:
                # point is [timestamp_ms, value]
                timestamp_s = point[0] / 1000
                datapoints_2.append(MetricDatapoint(
                    timestamp=datetime.fromtimestamp(timestamp_s).isoformat(),
                    value=float(point[1]) if point[1] is not None else 0.0, # Handle None values
                    dimensions=filter_set_2
                ))

    return {
        "series_1": datapoints_1,
        "series_2": datapoints_2
    }
