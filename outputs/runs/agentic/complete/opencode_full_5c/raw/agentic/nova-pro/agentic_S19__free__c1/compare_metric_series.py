import boto3


def compare_metric_series(metric_name, start_time, end_time, dimensions1, dimensions2):
    cloudwatch = boto3.client("cloudwatch")
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": metric_name,
                        "Dimensions": dimensions1,
                    },
                    "Period": 300,
                    "Stat": "Average",
                },
            },
            {
                "Id": "m2",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": metric_name,
                        "Dimensions": dimensions2,
                    },
                    "Period": 300,
                    "Stat": "Average",
                },
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return response
