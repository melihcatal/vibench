import boto3

cw_client = boto3.client("cloudwatch")


def compare_metric_series(
    metric_name, start_time, end_time, dimension_name, dimension_values
):
    metric_queries = [
        {
            "Id": f"m{i + 1}",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/EC2",
                    "MetricName": metric_name,
                    "Dimensions": [{"Name": dimension_name, "Value": value}],
                },
                "Period": 300,
                "Stat": "Average",
            },
        }
        for i, value in enumerate(dimension_values)
    ]
    response = cw_client.get_metric_data(
        MetricDataQueries=metric_queries, StartTime=start_time, EndTime=end_time
    )
    return response
