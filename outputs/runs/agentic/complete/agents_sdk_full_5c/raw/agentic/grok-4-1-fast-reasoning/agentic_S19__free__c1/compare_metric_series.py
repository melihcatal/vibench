import boto3
import os
from datetime import datetime
from typing import Dict, Any, List
from observability_models import normalize_get_metric_data_result

def compare_metric_series(
    query1: Dict[str, Any],
    query2: Dict[str, Any],
    start_time: datetime,
    end_time: datetime,
    period: int = 60
) -> Dict[str, List[float]]:
    client = boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    mdq1 = {
        'Id': 'series1',
        'MetricStat': {
            'Metric': {
                'Namespace': query1['namespace'],
                'MetricName': query1['metric_name'],
                'Dimensions': query1.get('dimensions', [])
            },
            'Period': period,
            'Stat': 'Average'
        },
        'ReturnData': True
    }
    mdq2 = {
        'Id': 'series2',
        'MetricStat': {
            'Metric': {
                'Namespace': query2['namespace'],
                'MetricName': query2['metric_name'],
                'Dimensions': query2.get('dimensions', [])
            },
            'Period': period,
            'Stat': 'Average'
        },
        'ReturnData': True
    }
    response = client.get_metric_data(
        MetricDataQueries=[mdq1, mdq2],
        StartTime=start_time,
        EndTime=end_time
    )
    series1_data = normalize_get_metric_data_result(response['MetricDataResults'][0])
    series2_data = normalize_get_metric_data_result(response['MetricDataResults'][1])
    series1 = [d['value'] for d in series1_data]
    series2 = [d['value'] for d in series2_data]
    differences = [s1 - s2 for s1, s2 in zip(series1, series2)]
    return {
        'series1': series1,
        'series2': series2,
        'differences': differences
    }
