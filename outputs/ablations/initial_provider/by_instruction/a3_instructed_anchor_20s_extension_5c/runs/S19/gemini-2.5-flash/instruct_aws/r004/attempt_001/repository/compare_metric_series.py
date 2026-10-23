import datetime
from typing import Dict, Tuple
from observability_client import CloudWatchClient
from observability_models import MetricQuery, MetricDataPoint, MetricDataResponse

def compare_metric_series(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int, # in seconds
    statistic: str = 'Average',
    dimensions_series_1: Dict[str, str] = None,
    dimensions_series_2: Dict[str, str] = None,
    region_name: str = 'us-east-1'
) -> Tuple[MetricDataResponse, MetricDataResponse]:
    
    cloudwatch_client = CloudWatchClient(region_name=region_name).get_cloudwatch_client()

    # Query for series 1
    aws_dimensions_1 = [{"Name": k, "Value": v} for k, v in (dimensions_series_1 or {}).items()]
    response_1 = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=aws_dimensions_1,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic]
    )

    datapoints_1 = []
    unit_1 = None
    if 'Datapoints' in response_1:
        for dp in response_1['Datapoints']:
            datapoints_1.append(MetricDataPoint(timestamp=dp['Timestamp'], value=dp[statistic], unit=dp.get('Unit')))
            if unit_1 is None and 'Unit' in dp:
                unit_1 = dp['Unit']
    metric_query_1 = MetricQuery(namespace=namespace, metric_name=metric_name, dimensions=dimensions_series_1)
    series_1_data = MetricDataResponse(metric_query=metric_query_1, datapoints=datapoints_1, unit=unit_1)

    # Query for series 2
    aws_dimensions_2 = [{"Name": k, "Value": v} for k, v in (dimensions_series_2 or {}).items()]
    response_2 = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=aws_dimensions_2,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic]
    )

    datapoints_2 = []
    unit_2 = None
    if 'Datapoints' in response_2:
        for dp in response_2['Datapoints']:
            datapoints_2.append(MetricDataPoint(timestamp=dp['Timestamp'], value=dp[statistic], unit=dp.get('Unit')))
            if unit_2 is None and 'Unit' in dp:
                unit_2 = dp['Unit']
    metric_query_2 = MetricQuery(namespace=namespace, metric_name=metric_name, dimensions=dimensions_series_2)
    series_2_data = MetricDataResponse(metric_query=metric_query_2, datapoints=datapoints_2, unit=unit_2)

    return series_1_data, series_2_data