import boto3

def metric_summary(metric_name, start_time, end_time):
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{'Name': 'InstanceId', 'Value': 'i-0123456789abcdef0'}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum', 'Average', 'SampleCount', 'Minimum', 'Maximum'])
    datapoints = response['Datapoints']
    summary = {
        'sum': sum(dp['Sum'] for dp in datapoints if 'Sum' in dp),
        'average': sum(dp['Average'] for dp in datapoints if 'Average' in dp) / len(datapoints),
        'sample_count': sum(dp['SampleCount'] for dp in datapoints if 'SampleCount' in dp),
       'minimum': min(dp['Minimum'] for dp in datapoints if 'Minimum' in dp),
       'maximum': max(dp['Maximum'] for dp in datapoints if 'Maximum' in dp)
    }
    return summary