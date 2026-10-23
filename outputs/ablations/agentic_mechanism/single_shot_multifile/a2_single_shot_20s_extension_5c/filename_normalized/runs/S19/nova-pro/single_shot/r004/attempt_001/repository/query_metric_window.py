import boto3

def query_metric_window(namespace, metric_name, start_time, end_time):
    client = boto3.client('cloudwatch')
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id':'m1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name
                    },
                    'Period': 300,
                    'Stat': 'Average'
                }
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )
    return response['MetricDataResults']