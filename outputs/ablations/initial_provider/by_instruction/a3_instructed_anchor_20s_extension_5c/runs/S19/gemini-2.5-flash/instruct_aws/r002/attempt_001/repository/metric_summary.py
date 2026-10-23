import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from observability_client import get_cloudwatch_client
from observability_models import MetricQuery

def summarize_metric_trends(
    metric_query: MetricQuery,
    end_time: datetime,
    lookback_minutes: int = 60,
    period: int = 300, # 5 minutes
    statistic: str = "Average",
) -> Dict[str, Any]:
    """
    Summarize recent metric trends using AWS CloudWatch.
    """
    cloudwatch = get_cloudwatch_client()
    start_time = end_time - timedelta(minutes=lookback_minutes)

    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': metric_query.to_cloudwatch_metric(),
                    'Period': period,
                    'Stat': statistic,
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    summary = {
        'metric_name': metric_query.metric_name,
        'namespace': metric_query.namespace,
        'datapoints_count': 0,
        'average': None,
        'maximum': None,
        'minimum': None,
        'last_value': None,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
    }

    if response and response.get('MetricDataResults'):
        for result in response['MetricDataResults']:
            if result.get('Values') and result.get('Timestamps'):
                values = result['Values']
                timestamps = result['Timestamps']
                if values:
                    summary['datapoints_count'] = len(values)
                    summary['average'] = sum(values) / len(values)
                    summary['maximum'] = max(values)
                    summary['minimum'] = min(values)
                    # Find the last value based on timestamp
                    if timestamps:
                        latest_timestamp_index = timestamps.index(max(timestamps))
                        summary['last_value'] = values[latest_timestamp_index]
    return summary
