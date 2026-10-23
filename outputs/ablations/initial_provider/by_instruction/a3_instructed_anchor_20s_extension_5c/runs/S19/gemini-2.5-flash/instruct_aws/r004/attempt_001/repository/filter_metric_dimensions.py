import datetime
from typing import Dict, List
from observability_client import CloudWatchClient
from observability_models import MetricQuery, MetricDataPoint, MetricDataResponse

def filter_metric_dimensions(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int, # in seconds
    statistic: str = 'Average',
    filter_dimensions: Dict[str, str] = None, # dimensions to filter by
    region_name: str = 'us-east-1'
) -> MetricDataResponse:
    
    cloudwatch_client = CloudWatchClient(region_name=region_name).get_cloudwatch_client()

    aws_dimensions = [{"Name": k, "Value": v} for k, v in (filter_dimensions or {}).items()]

    response = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=aws_dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic]
    )

    datapoints = []
    unit = None
    if 'Datapoints' in response:
        for dp in response['Datapoints']:
            datapoints.append(MetricDataPoint(timestamp=dp['Timestamp'], value=dp[statistic], unit=dp.get('Unit')))
            if unit is None and 'Unit' in dp:
                unit = dp['Unit']

    metric_query = MetricQuery(namespace=namespace, metric_name=metric_name, dimensions=filter_dimensions)
    return MetricDataResponse(metric_query=metric_query, datapoints=datapoints, unit=unit)