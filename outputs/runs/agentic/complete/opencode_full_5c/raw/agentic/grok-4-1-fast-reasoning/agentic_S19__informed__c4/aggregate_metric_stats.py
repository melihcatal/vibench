from typing import Dict, List
from datetime import datetime
from observability_client import get_cloudwatch_client


def aggregate_metric_stats(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    stats: List[str] = None,
    period: int = 300,
) -> Dict[str, float]:
    if stats is None:
        stats = ["Average", "Sum", "SampleCount", "Minimum", "Maximum"]
    client = get_cloudwatch_client()
    queries = []
    for i, st in enumerate(stats):
        queries.append(
            {
                "Id": f"s{i}",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                    },
                    "Period": period,
                    "Stat": st,
                },
            }
        )
    response = client.get_metric_data(
        MetricDataQueries=queries, StartTime=start_time, EndTime=end_time
    )
    result = {}
    for mdq, mdr in zip(queries, response["MetricDataResults"]):
        stat_id = mdq["Id"]
        if mdr["Values"]:
            result[stat_id] = mdr["Values"][-1]["Value"]
        else:
            result[stat_id] = None
    return result
