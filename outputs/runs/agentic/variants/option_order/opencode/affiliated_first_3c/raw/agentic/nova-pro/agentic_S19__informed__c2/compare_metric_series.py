import boto3


def compare_metric_series(metric_name, dimensions1, dimensions2, start_time, end_time):
    client = boto3.client("cloudwatch")
    response1 = client.get_metric_data(
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
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    response2 = client.get_metric_data(
        MetricDataQueries=[
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
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return response1, response2
