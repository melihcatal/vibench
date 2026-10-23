from datetime import datetime, timezone
from typing import Dict, Any, List

from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint, MetricSeries

def filter_metric_dimensions(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, List[MetricSeries]]:
    config = config or {}
    client = get_cloudwatch_client(config.get("region"))

    metric_queries = [
        {
            "Id": "m1",
            "MetricStat": {
                "Metric": {
                    "Namespace": config["namespace"],
                    "MetricName": payload["metric"],
                    "Dimensions": [{"Name": k, "Value": v} for k, v in payload.get("dimensions", {}).items()]
                },
                "Period": config.get("period_seconds", 60),
                "Stat": payload.get("statistic", "Average"),
            },
            "ReturnData": True,
        }
    ]

    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
    )

    metric_series_list = []
    for result in response["MetricDataResults"]:
        points = [
            MetricDatapoint(timestamp=timestamp.timestamp(), value=value)
            for timestamp, value in zip(result["Timestamps"], result["Values"])
        ]
        metric_series_list.append(MetricSeries(label=result["Label"], points=points))

    return {"metric_series": metric_series_list}
