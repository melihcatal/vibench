import datetimerom typing import List, Dictrom observability_client import CloudWatchClientrom observability_models import MetricQuery, MetricDataPoint, MetricDataResponse

def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int, # in seconds
    statistics: List[str], # e.g., ['Average', 'Sum', 'Maximum', 'Minimum']
    dimensions: Dict[str, str] = None,
    region_name: str = 'us-east-1'
) -> MetricDataResponse:
    
    cloudwatch_client = CloudWatchClient(region_name=region_name).get_cloudwatch_client()

    aws_dimensions = [{"Name": k, "Value": v} for k, v in (dimensions or {}).items()]

    response = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=aws_dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics
    )

    datapoints = []
    unit = None
    if 'Datapoints' in response:
        for dp in response['Datapoints']:
            for stat_name in statistics:
                if stat_name in dp:
                    datapoints.append(MetricDataPoint(timestamp=dp['Timestamp'], value=dp[stat_name], unit=dp.get('Unit')))
                    if unit is None and 'Unit' in dp:
                        unit = dp['Unit']

    metric_query = MetricQuery(namespace=namespace, metric_name=metric_name, dimensions=dimensions)
    return MetricDataResponse(metric_query=metric_query, datapoints=datapoints, unit=unit)