import boto3


def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = boto3.client('cloudwatch', region_name=config.get('region', 'us-east-1'))
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': payload['namespace'],
                        'MetricName': payload['metric_name']
                    },
                    'Period': config.get('period', 300),
                    'Stat': 'Average'
                }
            }
        ],
        TimeRange={'Start': payload['start_time'], 'End': payload['end_time']}
    )
    dimensions = response['MetricDataResults'][0]['Dimensions']
    return {'dimensions': dimensions}