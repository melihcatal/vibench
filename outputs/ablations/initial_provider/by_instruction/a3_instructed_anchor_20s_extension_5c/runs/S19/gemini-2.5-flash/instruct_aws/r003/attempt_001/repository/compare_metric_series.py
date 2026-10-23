from datetime import datetime
from typing import Dict, Any, List

from observability_client import ObservabilityClient
from observability_models import MetricQuery, MetricDataPoint, MetricQueryResult

def compare_metric_series(
    query_1: MetricQuery,
    query_2: MetricQuery
) -> Dict[str, List[MetricDataPoint]]:
    client = ObservabilityClient()

    # Query for the first metric series
    metric_data_results_1 = client.query_metric_data(
        namespace=query_1.namespace,
        metric_name=query_1.metric_name,
        dimensions=query_1.dimensions,
        start_time=query_1.start_time,
        end_time=query_1.end_time,
        period=query_1.period
    )
    datapoints_1 = []
    for result in metric_data_results_1:
        if result.get('Values') and result.get('Timestamps'):
            for i in range(len(result['Values'])):
                datapoints_1.append(MetricDataPoint(
                    timestamp=result['Timestamps'][i],
                    value=float(result['Values'][i]),
                    unit=result.get('Unit', 'Unknown')
                ))
    datapoints_1.sort(key=lambda dp: dp.timestamp)

    # Query for the second metric series
    metric_data_results_2 = client.query_metric_data(
        namespace=query_2.namespace,
        metric_name=query_2.metric_name,
        dimensions=query_2.dimensions,
        start_time=query_2.start_time,
        end_time=query_2.end_time,
        period=query_2.period
    )
    datapoints_2 = []
    for result in metric_data_results_2:
        if result.get('Values') and result.get('Timestamps'):
            for i in range(len(result['Values'])):
                datapoints_2.append(MetricDataPoint(
                    timestamp=result['Timestamps'][i],
                    value=float(result['Values'][i]),
                    unit=result.get('Unit', 'Unknown')
                ))
    datapoints_2.sort(key=lambda dp: dp.timestamp)

    return {
        f"{query_1.metric_name}_series_1": datapoints_1,
        f"{query_2.metric_name}_series_2": datapoints_2,
    }
