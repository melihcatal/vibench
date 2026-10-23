from observability_client import get_cloudwatch_client
from observability_models import MetricQuery, MetricDatapoint, MetricQueryResult
from datetime import datetime

def query_metric_window(query: MetricQuery) -> MetricQueryResult:
    cloudwatch = get_cloudwatch_client()

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
    
    # Sort datapoints by timestamp as CloudWatch might not return them sorted
    datapoints.sort(key=lambda x: x.timestamp)

    return MetricQueryResult(
        label=query.metric_name,
        datapoints=datapoints,
        status_code=response['ResponseMetadata']['HTTPStatusCode']
    )
