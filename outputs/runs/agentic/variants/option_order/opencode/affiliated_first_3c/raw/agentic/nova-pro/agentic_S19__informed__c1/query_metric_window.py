import boto3


def query_metric_window(metric_name, start_time, end_time):
    cloudwatch = boto3.client("cloudwatch")
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {"Namespace": "AWS/EC2", "MetricName": metric_name},
                    "Period": 300,
                    "Stat": "Average",
                },
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return response
