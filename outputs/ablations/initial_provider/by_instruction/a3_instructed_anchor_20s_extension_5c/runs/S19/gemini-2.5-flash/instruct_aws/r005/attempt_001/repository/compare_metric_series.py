from observability_client import get_cloudwatch_client
from observability_models import MetricQuery, MetricDatapoint, MetricQueryResult
from datetime import datetime
from typing import List, Dict, Any

def compare_metric_series(
    query1: MetricQuery,
    query2: MetricQuery
) -> Dict[str, MetricQueryResult]:
    cloudwatch = get_cloudwatch_client()

    def _get_metric_data(query: MetricQuery) -> MetricQueryResult:
        dimensions_list = []
        for name, value in query.dimensions.items():
            dimensions_list.append({'Name': name, 'Value': value})

        response = cloudwatch.get_metric_statistics(
            Namespace=query.namespace,
            MetricName=query.metric_name,
            Dimensions=dimensions_list,
            StartTime=query.start_time,
            EndTime=query.end_time,
            Period=query.period,
            Statistics=query.statistics
        )

        datapoints = []
        for dp in response.get('Datapoints', []):
            for stat in query.statistics:
                if stat in dp:
                    datapoints.append(
                        MetricDatapoint(
                            timestamp=dp['Timestamp'],
                            value=float(dp[stat]),
                            unit=dp.get('Unit', 'Unknown')
                        )
                    )
        
        datapoints.sort(key=lambda x: x.timestamp)

        return MetricQueryResult(
            label=query.metric_name + "-" + '_'.join(query.dimensions.values()),
            datapoints=datapoints,
            status_code=response['ResponseMetadata']['HTTPStatusCode']
        )

    result1 = _get_metric_data(query1)
    result2 = _get_metric_data(query2)

    return {
        "series1": result1,
        "series2": result2
    }
