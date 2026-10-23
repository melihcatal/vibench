from __future__ import annotations

from typing import Dict, Optional

from observability_client import get_cloudwatch_client, load_metric_window
from observability_models import MetricSeriesResponse, MetricDatapoint, to_rfc3339


def filter_metric_dimensions(
    metric_name: str,
    namespace: str,
    dimensions: Dict[str, str],
    minutes: int = 15,
    period: int = 60,
    stat: str = "Average",
    region_name: Optional[str] = None,
) -> MetricSeriesResponse:
    client = get_cloudwatch_client(region_name=region_name)
    query = load_metric_window(
        metric_name=metric_name,
        namespace=namespace,
        minutes=minutes,
        period=period,
        stat=stat,
        dimensions=dimensions,
    )
    metric_data_queries = [
        {
            "Id": "filteredmetric",
            "MetricStat": {
                "Metric": {
                    "Namespace": query.namespace,
                    "MetricName": query.metric_name,
                    "Dimensions": query.to_cloudwatch_dimensions(),
                },
                "Period": query.period,
                "Stat": query.stat,
            },
            "ReturnData": True,
        }
    ]
    response = client.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=query.start_time,
        EndTime=query.end_time,
        ScanBy="TimestampAscending",
    )
    result = response["MetricDataResults"][0]
    datapoints = [
        MetricDatapoint(
            timestamp=to_rfc3339(ts),
            value=float(val),
            unit=result.get("Label"),
            stat=stat,
            dimensions=dict(dimensions),
        )
        for ts, val in zip(result.get("Timestamps", []), result.get("Values", []))
    ]
    return MetricSeriesResponse(
        metric_name=metric_name,
        namespace=namespace,
        start_time=to_rfc3339(query.start_time),
        end_time=to_rfc3339(query.end_time),
        period=period,
        stat=stat,
        datapoints=datapoints,
    )
