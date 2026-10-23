from datetime import datetime, timedelta
from typing import List

from observability_client import ObservabilityClient
from observability_models import MetricQuery, MetricDataPoint, MetricQueryResult

def query_metric_window(query: MetricQuery) -> MetricQueryResult:
    client = ObservabilityClient()
    metric_data_results = client.query_metric_data(
        namespace=query.namespace,
        metric_name=query.metric_name,
        dimensions=query.dimensions,
        start_time=query.start_time,
        end_time=query.end_time,
        period=query.period
    )

    datapoints = []
    for result in metric_data_results:
        if result.get('Values') and result.get('Timestamps'):
            for i in range(len(result['Values'])):
                datapoints.append(MetricDataPoint(
                    timestamp=result['Timestamps'][i],
                    value=float(result['Values'][i]),
                    unit=result.get('Unit', 'Unknown')
                ))
    
    # Sort datapoints by timestamp if they are not already sorted
    datapoints.sort(key=lambda dp: dp.timestamp)

    return MetricQueryResult(
        metric_name=query.metric_name,
        datapoints=datapoints
    )
