from datetime import datetime, timedelta
import os

from observability_client import get_cloudwatch_client


def query_metric_window(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,  # in seconds, default to 5 minutes
):
    client = get_cloudwatch_client()

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {"MetricName": metric_name, "Namespace": namespace},
                    "Period": period,
                    "Stat": "Average",
                },
                "ReturnData": True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return response
