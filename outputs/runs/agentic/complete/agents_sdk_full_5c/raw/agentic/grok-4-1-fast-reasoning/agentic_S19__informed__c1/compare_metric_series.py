import boto3
from datetime import datetime
from typing import List, Tuple
from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint, MetricDimension

def compare_metric_series(
    metric_name: str,
    dimensions1: List[MetricDimension],
    dimensions2: List[MetricDimension],
    start_time: datetime,
    end_time: datetime,
    namespace: str = 'AWS/EC2',
    period: int = 300,
    region: str = None
) -> Dict[str, List[float]]:
    client = get_cloudwatch_client(region)
    
    # Query first series
    dims1 = [{'Name': d.name, 'Value': d.value} for d in dimensions1]
    resp1 = client.get_metric_data(
        MetricDataQueries=[{
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': dims1
                },
                'Period': period,
                'Stat': 'Average'
            },
            'ReturnData': True
        }],
        StartTime=start_time,
        EndTime=end_time
    )
    values1 = resp1['MetricDataResults'][0]['Values']
    
    # Query second series
    dims2 = [{'Name': d.name, 'Value': d.value} for d in dimensions2]
    resp2 = client.get_metric_data(
        MetricDataQueries=[{
            'Id': 'm2',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': dims2
                },
                'Period': period,
                'Stat': 'Average'
            },
            'ReturnData': True
        }],
        StartTime=start_time,
        EndTime=end_time
    )
    values2 = resp2['MetricDataResults'][0]['Values']
    
    # Pad shorter list
    max_len = max(len(values1), len(values2))
    values1 += [None] * (max_len - len(values1))
    values2 += [None] * (max_len - len(values2))
    
    diffs = []
    ratios = []
    for v1, v2 in zip(values1, values2):
        if v1 is not None and v2 is not None and v2 != 0:
            diff = v1 - v2
            ratio = v1 / v2
            diffs.append(diff)
            ratios.append(ratio)
        else:
            diffs.append(None)
            ratios.append(None)
    
    return {
        'series1': values1,
        'series2': values2,
        'diffs': diffs,
        'ratios': ratios
    }
