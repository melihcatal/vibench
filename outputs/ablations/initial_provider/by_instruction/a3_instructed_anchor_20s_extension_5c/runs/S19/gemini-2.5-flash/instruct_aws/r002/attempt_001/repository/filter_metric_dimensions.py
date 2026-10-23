import os
from datetime import datetime
from typing import List, Dict, Any
from observability_client import get_cloudwatch_client
from observability_models import MetricQuery

def filter_metric_dimensions(
    metric_query: MetricQuery,
    start_time: datetime,
    end_time: datetime,
    period: int = 300, # 5 minutes
    statistic: str = "Average",
) -> List[Dict[str, Any]]:
    """
    Queries metric data filtered by resource labels or dimensions using AWS CloudWatch.
    """
    cloudwatch = get_cloudwatch_client()

    metric_data_queries = [{
        'Id': 'm1',
        'MetricStat': {
            'Metric': metric_query.to_cloudwatch_metric(),
            'Period': period,
            'Stat': statistic,
        },
        'ReturnData': True,
    }]

    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=start_time,
        EndTime=end_time,
    )

    datapoints = []
    if response and response.get('MetricDataResults'):
        for result in response['MetricDataResults']:
            if result.get('Values') and result.get('Timestamps'):
                for i in range(len(result['Values'])):
                    datapoints.append({
                        'timestamp': result['Timestamps'][i].isoformat(),
                        'value': result['Values'][i]
                    })
    return datapoints
