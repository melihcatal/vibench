import boto3

def aggregate_metric_stats(namespace, metric_name, start_time, end_time):
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-0abcd1234efgh5678'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average', 'Sum']
    )
    return response