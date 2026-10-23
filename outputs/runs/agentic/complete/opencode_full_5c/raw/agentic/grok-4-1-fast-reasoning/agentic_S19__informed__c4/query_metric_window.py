from typing import List
from datetime import datetime
from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint


def query_metric_window(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    stat: str = "Average",
) -> List[MetricDatapoint]:
    client = get_cloudwatch_client()
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                    },
                    "Period": period,
                    "Stat": stat,
                },
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        ScanBy="Timestamp",
    )
    if response["MetricDataResults"]:
        return response["MetricDataResults"][0]["Values"]
    return []
