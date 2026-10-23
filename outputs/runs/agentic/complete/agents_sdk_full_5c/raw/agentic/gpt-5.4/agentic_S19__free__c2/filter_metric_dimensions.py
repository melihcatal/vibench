from __future__ import annotations

from typing import Dict, List

from observability_client import cloudwatch_client


CLOUDWATCH_API = "cloudwatch.amazonaws.com"


def filter_metric_dimensions(
    namespace: str,
    metric_name: str,
    start_time,
    end_time,
    period: int,
    stat: str,
    dimensions: Dict[str, str],
) -> List[dict]:
    client = cloudwatch_client()
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "filteredmetric",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": [{"Name": name, "Value": value} for name, value in dimensions.items()],
                    },
                    "Period": period,
                    "Stat": stat,
                },
                "ReturnData": True,
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        ScanBy="TimestampAscending",
    )
    result = response.get("MetricDataResults", [{}])[0]
    timestamps = result.get("Timestamps", [])
    values = result.get("Values", [])
    return [
        {
            "timestamp": ts,
            "value": value,
            "dimensions": dimensions,
            "provider": CLOUDWATCH_API,
        }
        for ts, value in zip(timestamps, values)
    ]
