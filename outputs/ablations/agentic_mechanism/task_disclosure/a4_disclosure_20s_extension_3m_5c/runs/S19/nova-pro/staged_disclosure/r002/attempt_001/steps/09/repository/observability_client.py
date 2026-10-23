import boto3
import os

# Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

# Client
cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION)

# Utility Functions
def put_metric_data(namespace, metric_data):
    response = cloudwatch.put_metric_data(
        Namespace=namespace,
        MetricData=metric_data
    )
    return response

def get_metric_statistics(namespace, metric_name, dimensions, start_time, end_time, period, statistics):
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics
    )
    return response