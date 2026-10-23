import boto3


def compare_metric_series(
    metric_name,
    start_time,
    end_time,
    dimension_name,
    dimension_value1,
    dimension_value2,
):
    client = boto3.client("cloudwatch")
    response1 = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[{"Name": dimension_name, "Value": dimension_value1}],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Average"],
    )
    response2 = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[{"Name": dimension_name, "Value": dimension_value2}],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Average"],
    )
    return response1, response2
