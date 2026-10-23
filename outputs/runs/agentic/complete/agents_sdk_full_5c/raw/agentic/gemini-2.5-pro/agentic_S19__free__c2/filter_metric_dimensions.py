import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

from observability_client import ClientFactory
from observability_models import MetricData, TimeSeriesPoint


def get_cloudwatch_metric_with_dimensions(
    namespace: str,
    metric_name: str,
    dimensions: List[Dict[str, str]],
    minutes_ago: int = 60,
) -> List[MetricData]:
    """
    Queries AWS CloudWatch for metric data, filtered by dimensions.

    Args:
        namespace: The CloudWatch namespace (e.g., 'AWS/EC2').
        metric_name: The name of the metric (e.g., 'CPUUtilization').
        dimensions: A list of dimension dictionaries (e.g., [{'Name': 'InstanceId', 'Value': 'i-12345'}]).
        minutes_ago: The number of minutes in the past to query.

    Returns:
        A list of MetricData objects.
    """
    client = ClientFactory.get_aws_cloudwatch_client()
    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)

    metric_data_queries = [
        {
            "Id": f"query{i}",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                    "Dimensions": [dim],
                },
                "Period": 300,  # 5-minute intervals
                "Stat": "Average",
            },
            "ReturnData": True,
        }
        for i, dim in enumerate(dimensions)
    ]

    response = client.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=start_time,
        EndTime=now,
    )

    results = []
    for metric_data_result in response.get("MetricDataResults", []):
        if "Timestamps" in metric_data_result and "Values" in metric_data_result:
            points = [
                TimeSeriesPoint(timestamp=ts.timestamp(), value=val)
                for ts, val in zip(metric_data_result["Timestamps"], metric_data_result["Values"])
            ]
            # Find corresponding dimension for this result
            query_id = metric_data_result["Id"]
            query_index = int(query_id.replace("query", ""))
            dimension_dict = {d['Name']: d['Value'] for d in dimensions[query_index]}

            results.append(
                MetricData(
                    metric_name=metric_name,
                    points=points,
                    dimensions=dimension_dict,
                )
            )
    return results

# Example usage would require AWS credentials configured.
# if __name__ == '__main__':
#     if os.environ.get("AWS_ACCESS_KEY_ID"):
#         # Replace with your actual instance IDs
#         instance_dimensions = [
#             {'Name': 'InstanceId', 'Value': 'i-0abcdef1234567890'},
#             {'Name': 'InstanceId', 'Value': 'i-0987654321fedcba0'}
#         ]
#         data = get_cloudwatch_metric_with_dimensions(
#             namespace='AWS/EC2',
#             metric_name='CPUUtilization',
#             dimensions=instance_dimensions,
#             minutes_ago=120
#         )
#         for series in data:
#             print(f"Filtered series for dimensions: {series.dimensions}")
#             for point in series.points:
#                 print(f"  - Time: {point.timestamp}, Value: {point.value}")
#     else:
#         print("AWS credentials (e.g., AWS_ACCESS_KEY_ID) not found in environment.")
