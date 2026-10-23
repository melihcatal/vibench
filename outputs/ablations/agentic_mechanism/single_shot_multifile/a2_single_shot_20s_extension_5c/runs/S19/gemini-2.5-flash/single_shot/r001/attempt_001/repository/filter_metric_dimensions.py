import os
from datetime import datetime, timedelta
from azure.monitor.query import MonitorQueryClient, MetricAggregationType
from azure.identity import DefaultAzureCredential

def filter_metric_dimensions(resource_id: str, metric_name: str, aggregation_type: str, minutes_ago: int = 60, time_grain: str = 'PT1M', filter_expression: str = None) -> list:
    credential = DefaultAzureCredential()
    client = MonitorQueryClient(credential=credential)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes_ago)

    # Map string aggregation type to MetricAggregationType enum
    aggregation_map = {
        'average': MetricAggregationType.AVERAGE,
        'total': MetricAggregationType.TOTAL,
        'minimum': MetricAggregationType.MINIMUM,
        'maximum': MetricAggregationType.MAXIMUM,
        'count': MetricAggregationType.COUNT
    }
    agg_type_enum = aggregation_map.get(aggregation_type.lower())
    if not agg_type_enum:
        raise ValueError(f"Unsupported aggregation type: {aggregation_type}")

    response = client.query_resource_metrics(
        resource_id=resource_id,
        metric_names=[metric_name],
        timespan=(start_time, end_time),
        aggregations=[agg_type_enum],
        granularity=timedelta(minutes=int(time_grain.replace('PT', '').replace('M', ''))),
        filter=filter_expression
    )

    results = []
    for metric in response.metrics:
        for time_series in metric.timeseries:
            for data_point in time_series.data:
                results.append({
                    "timestamp": data_point.timestamp.isoformat(),
                    "value": getattr(data_point, aggregation_type.lower(), None),
                    "metric_name": metric.name,
                    "dimensions": {d.name: d.value for d in time_series.metadata}
                })
    return results