import boto3
from typing import List, Dict, Any, Optional
from observability_client import get_aws_region, make_dimensions, create_recent_window
from observability_models import parse_datapoints, MetricDatapoint

def _get_datapoints(client: boto3.client, metric_name: str, window: Dict[str, datetime], dims: List[Dict[str, str]], period: int, statistics: List[str]) -> List[MetricDatapoint]:
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        StartTime=window['start'],
        EndTime=window['end'],
        Period=period,
        Statistics=statistics,
        Dimensions=dims
    )
    return parse_datapoints(response['Datapoints'])

def compare_metric_series(
    metric_name: str,
    duration_minutes: int = 60,
    dimensions_a: List[Dict[str, str]],
    dimensions_b: List[Dict[str, str]],
    period: int = 300,
    statistics: List[str] = ['Average']
) -> Dict[str, Any]:
    region = get_aws_region()
    client = boto3.client('cloudwatch', region_name=region)
    window = create_recent_window(duration_minutes)
    dims_a = make_dimensions(dimensions_a)
    dims_b = make_dimensions(dimensions_b)
    points_a = _get_datapoints(client, metric_name, window, dims_a, period, statistics)
    points_b = _get_datapoints(client, metric_name, window, dims_b, period, statistics)
    if points_a and points_b:
        last_a = points_a[-1].average or 0.0
        last_b = points_b[-1].average or 0.0
        ratio = last_a / last_b if last_b != 0 else float('inf')
        return {
            'series_a_last': last_a,
            'series_b_last': last_b,
            'difference': last_a - last_b,
            'ratio_a_over_b': ratio
        }
    return {'error': 'No data available for comparison'}
