import os
from datetime import datetime
from typing import List, Dict, Any
from observability_client import get_cloudwatch_client
from observability_models import MetricQuery

def compare_metric_series(
    metric_query1: MetricQuery,
    metric_query2: MetricQuery,
    start_time: datetime,
    end_time: datetime,
    period: int = 300, # 5 minutes
    statistic: str = "Average",
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Compares metric values for two resources or dimension filters over the same window using AWS CloudWatch.
    """
    cloudwatch = get_cloudwatch_client()

    metric_data_queries = [
        {
            'Id': 'm1',
            'MetricStat': {
                'Metric': metric_query1.to_cloudwatch_metric(),
                'Period': period,
                'Stat': statistic,
            },
            'ReturnData': True,
            'Label': 'Metric Series 1'
        },
        {
            'Id': 'm2',
            'MetricStat': {
                'Metric': metric_query2.to_cloudwatch_metric(),
                'Period': period,
                'Stat': statistic,
            },
            'ReturnData': True,
            'Label': 'Metric Series 2'
        },
    ]

    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=start_time,
        EndTime=end_time,
    )

    comparison_results = {
        'series1': [],
        'series2': [],
    }

    if response and response.get('MetricDataResults'):
        for result in response['MetricDataResults']:
            series_id = result.get('Id')
            datapoints = []
            if result.get('Values') and result.get('Timestamps'):
                for i in range(len(result['Values'])):
                    datapoints.append({
                        'timestamp': result['Timestamps'][i].isoformat(),
                        'value': result['Values'][i]
                    })
            if series_id == 'm1':
                comparison_results['series1'] = datapoints
            elif series_id == 'm2':
                comparison_results['series2'] = datapoints
    return comparison_results
