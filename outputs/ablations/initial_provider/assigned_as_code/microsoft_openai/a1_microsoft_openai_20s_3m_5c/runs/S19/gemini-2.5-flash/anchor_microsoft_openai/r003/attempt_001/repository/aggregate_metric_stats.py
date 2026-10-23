from datetime import datetime, timedelta, timezone
from azure.monitor.query import MetricAggregationType
from observability_client import get_metrics_query_client
from observability_models import AggregatedMetricValue, MetricAggregationResult

def aggregate_metric_stats(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)

    aggregations = []
    if payload.get('include_average', False): aggregations.append(MetricAggregationType.AVERAGE)
    if payload.get('include_minimum', False): aggregations.append(MetricAggregationType.MINIMUM)
    if payload.get('include_maximum', False): aggregations.append(MetricAggregationType.MAXIMUM)
    if payload.get('include_total', False): aggregations.append(MetricAggregationType.TOTAL)
    if payload.get('include_count', False): aggregations.append(MetricAggregationType.COUNT)

    if not aggregations: # Default to average if no specific aggregations are requested
        aggregations.append(MetricAggregationType.AVERAGE)

    client = get_metrics_query_client()
    with client:
        result = client.query_resource(
            resource_id=config['resource_id'],
            metric_names=[payload['metric']],
            timespan=(start, end),
            granularity=timedelta(seconds=config.get('period_seconds', 60)),
            aggregations=aggregations,
        )

    all_aggregated_values = []
    for metric_result in result.metrics:
        for timeseries_element in metric_result.timeseries:
            for data_point in timeseries_element.data:
                all_aggregated_values.append(AggregatedMetricValue(
                    timestamp=data_point.timestamp.timestamp(),
                    average=data_point.average,
                    minimum=data_point.minimum,
                    maximum=data_point.maximum,
                    total=data_point.total,
                    count=data_point.count
                ))

    # Assuming one metric name is queried, and we return a single aggregated result.
    # For simplicity, if multiple timeseries are returned (e.g., due to dimensions),
    # this example aggregates all into one list of values. A more complex scenario
    # might separate by dimensions.
    if result.metrics:
        first_metric = result.metrics[0]
        return MetricAggregationResult(
            name=first_metric.name,
            unit=first_metric.unit,
            values=sorted(all_aggregated_values, key=lambda x: x.timestamp)
        )
    return MetricAggregationResult(name=payload['metric'], unit="unknown", values=[])
