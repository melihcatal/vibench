from __future__ import annotations

from typing import Dict

from observability_client import cloudwatch_client
from observability_models import ComparisonResult, Datapoint, average_of_points


AWS_CLOUDWATCH = "AWS CloudWatch"


def compare_metric_series(
    namespace: str,
    metric_name: str,
    start_time,
    end_time,
    period: int,
    stat: str,
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
) -> ComparisonResult:
    client = cloudwatch_client()
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "leftseries",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": [{"Name": k, "Value": v} for k, v in left_dimensions.items()],
                    },
                    "Period": period,
                    "Stat": stat,
                },
                "Label": "left",
                "ReturnData": True,
            },
            {
                "Id": "rightseries",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": [{"Name": k, "Value": v} for k, v in right_dimensions.items()],
                    },
                    "Period": period,
                    "Stat": stat,
                },
                "Label": "right",
                "ReturnData": True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        ScanBy="TimestampAscending",
    )
    results = {item["Id"]: item for item in response.get("MetricDataResults", [])}

    def to_points(item, dims):
        return [
            Datapoint(timestamp=ts, value=value, dimensions=dims, raw={"provider": AWS_CLOUDWATCH})
            for ts, value in zip(item.get("Timestamps", []), item.get("Values", []))
        ]

    left_points = to_points(results.get("leftseries", {}), left_dimensions)
    right_points = to_points(results.get("rightseries", {}), right_dimensions)
    left_avg = average_of_points(left_points)
    right_avg = average_of_points(right_points)
    delta = None if left_avg is None or right_avg is None else left_avg - right_avg
    return ComparisonResult(
        left_label=str(left_dimensions),
        right_label=str(right_dimensions),
        left_points=left_points,
        right_points=right_points,
        delta_average=delta,
    )
