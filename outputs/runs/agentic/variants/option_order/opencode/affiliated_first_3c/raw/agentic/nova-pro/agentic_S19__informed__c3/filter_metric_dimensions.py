import boto3


def filter_metric_dimensions(metric_name, start_time, end_time, dimensions):
    cloudwatch = boto3.client("cloudwatch")
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )
    return response
