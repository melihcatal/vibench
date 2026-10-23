import boto3
from observability_client import create_cw_client

cw_client = create_cw_client()


def metric_summary(metric_name, start_time, end_time):
    response = cw_client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": metric_name,
                        "Dimensions": [
                            {"Name": "InstanceId", "Value": "i-0123456789abcdef0"}
                        ],
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
