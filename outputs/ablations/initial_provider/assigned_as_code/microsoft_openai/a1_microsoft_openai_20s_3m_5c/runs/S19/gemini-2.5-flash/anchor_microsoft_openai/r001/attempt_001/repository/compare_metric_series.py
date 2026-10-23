from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType


def _query_series(client, resource_id, metric_name, timespan, granularity, filter_str=None):
    result = client.query_resource(resource_id, metric_names=[metric_name],
        timespan=timespan, granularity=granularity,
        aggregations=[MetricAggregationType.AVERAGE],
        filter=filter_str if filter_str else None)
    
    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
              for metric in result.metrics for series in metric.timeseries
              for point in series.data if point.average is not None]
    return sorted(points, key=lambda point: point['timestamp'])


def compare_metric_series(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    timespan = (start, end)
    granularity = timedelta(seconds=config.get('period_seconds', 60))

    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            series1_filter_str = None
            if 'series1_dimension_filters' in payload:
                filters1 = []
                for dim_name, dim_value in payload['series1_dimension_filters'].items():
                    filters1.append(f"{dim_name} eq '{dim_value}'")
                series1_filter_str = " and ".join(filters1)
            
            series1_data = _query_series(client, config['resource_id'], payload['metric'], timespan, granularity, series1_filter_str)

            series2_filter_str = None
            if 'series2_dimension_filters' in payload:
                filters2 = []
                for dim_name, dim_value in payload['series2_dimension_filters'].items():
                    filters2.append(f"{dim_name} eq '{dim_value}'")
                series2_filter_str = " and ".join(filters2)
            
            series2_data = _query_series(client, config['resource_id'], payload['metric'], timespan, granularity, series2_filter_str)
    
    return {
        'series1': series1_data,
        'series2': series2_data
    }
