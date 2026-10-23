import boto3

def compare_metric_series(namespace, metric_name, dimension_name, dimension_values, start_time, end_time):
    cloudwatch = boto3.client('cloudwatch')
    
    response1 = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': dimension_values[0]
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    
    response2 = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[{
            'Name': dimension_name,
            'Value': dimension_values[1]
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    
    print(f'Metrics for {dimension_values[0]}: {response1}')
    print(f'Metrics for {dimension_values[1]}: {response2}')
    
    # Additional comparison logic can be added here
