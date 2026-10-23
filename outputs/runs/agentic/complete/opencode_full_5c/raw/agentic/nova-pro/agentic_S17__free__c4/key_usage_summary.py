import boto3

cloudwatch = boto3.client("cloudwatch", region_name="us-west-2")


def key_usage_summary():
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "kmsUsage",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/KMS",
                        "MetricName": "EncryptDecryptEvents",
                    },
                    "Period": 3600,
                    "Stat": "Sum",
                },
            }
        ],
        StartTime="2026-04-12T00:00:00",
        EndTime="2026-04-19T00:00:00",
    )
    return response["MetricDataResults"][0]["Values"]
