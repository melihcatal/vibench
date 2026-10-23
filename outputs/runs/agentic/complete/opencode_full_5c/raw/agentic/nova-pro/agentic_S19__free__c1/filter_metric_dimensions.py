import boto3


def filter_metric_dimensions(metric_name, start_time, end_time, dimensions):
    cloudwatch = boto3.client("cloudwatch")
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": metric_name,
                        "Dimensions": dimensions,
                    },
                    "Period": 300,
                    "Stat": "Average",
                },
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return response
