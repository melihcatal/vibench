from typing import Dict, Any
from datetime import datetime
from observability_client import get_cloudwatch_client
from observability_models import Dimension


def compare_metric_series(
    metric_name: str,
    namespace: str,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    stat: str = "Average",
) -> Dict[str, Any]:
    client = get_cloudwatch_client()
    dims1 = [{"Name": k, "Value": v} for k, v in dimensions1.items()]
    dims2 = [{"Name": k, "Value": v} for k, v in dimensions2.items()]
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "r1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": dims1,
                    },
                    "Period": period,
                    "Stat": stat,
                },
            },
            {
                "Id": "r2",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": dims2,
                    },
                    "Period": period,
                    "Stat": stat,
                },
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    val1 = None
    val2 = None
    if response["MetricDataResults"] and response["MetricDataResults"][0]["Values"]:
        val1 = response["MetricDataResults"][0]["Values"][-1]["Value"]
    if (
        len(response["MetricDataResults"]) > 1
        and response["MetricDataResults"][1]["Values"]
    ):
        val2 = response["MetricDataResults"][1]["Values"][-1]["Value"]
    return {
        "series1_last": val1,
        "series2_last": val2,
        "difference": val1 - val2 if val1 is not None and val2 is not None else None,
    }
