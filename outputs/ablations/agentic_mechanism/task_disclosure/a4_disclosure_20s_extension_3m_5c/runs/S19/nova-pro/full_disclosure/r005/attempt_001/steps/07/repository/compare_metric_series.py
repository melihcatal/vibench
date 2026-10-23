import boto3

def compare_metric_series(metric_name, resource_id1, resource_id2, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    
    response1 = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': resource_id1
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    
    response2 = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': resource_id2
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    
    return response1, response2