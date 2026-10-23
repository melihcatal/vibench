from datetime import datetime, timezone
from typing import Dict, Any, List

from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint, MetricSeries

def compare_metric_series(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, List[MetricSeries]]:
    config = config or {}
    client = get_cloudwatch_client(config.get("region"))

    metric_queries = [
        {
            "Id": "m1",
            "MetricStat": {
                "Metric": {
                    "Namespace": config["namespace"],
                    "MetricName": payload["metric"],
                    "Dimensions": [{"Name": k, "Value": v} for k, v in payload.get("dimensions_1", {}).items()]
                },
                "Period": config.get("period_seconds", 60),
                "Stat": payload.get("statistic", "Average"),
            },
            "Label": payload.get("label_1", "Series 1"),
            "ReturnData": True,
        },
        {
            "Id": "m2",
            "MetricStat": {
                "Metric": {
                    "Namespace": config["namespace"],
                    "MetricName": payload["metric"],
                    "Dimensions": [{"Name": k, "Value": v} for k, v in payload.get("dimensions_2", {}).items()]
                },
                "Period": config.get("period_seconds", 60),
                "Stat": payload.get("statistic", "Average"),
            },
            "Label": payload.get("label_2", "Series 2"),
            "ReturnData": True,
        }
    ]

    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
    )

    compared_series = []
    for result in response["MetricDataResults"]:
        points = [
            MetricDatapoint(timestamp=timestamp.timestamp(), value=value)
            for timestamp, value in zip(result["Timestamps"], result["Values"])
        ]
        compared_series.append(MetricSeries(label=result["Label"], points=points))

    return {"compared_metric_series": compared_series}
