import boto3

def summarize_metric_trends(namespace, metric_name, period=3600):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': 'i-0abcd1234efgh5678'
        }],
        StartTime=(datetime.utcnow() - timedelta(hours=6)),
        EndTime=datetime.utcnow(),
        Period=period,
        Statistics=['Average', 'Sum']
    )
    return response['Datapoints'] if 'Datapoints' in response else []

def summarize_metric_anomalies(namespace, metric_name, period=3600):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[{
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': [{
                        'Name': 'InstanceId',
                        'Value': 'i-0abcd1234efgh5678'
                    }]
                },
                'Period': period,
                'Stat': 'Average'
            }
        }],
        StartTime=(datetime.utcnow() - timedelta(hours=6)),
        EndTime=datetime.utcnow()
    )
    return response['MetricDataResults'][0]['Values'] if 'MetricDataResults' in response else []