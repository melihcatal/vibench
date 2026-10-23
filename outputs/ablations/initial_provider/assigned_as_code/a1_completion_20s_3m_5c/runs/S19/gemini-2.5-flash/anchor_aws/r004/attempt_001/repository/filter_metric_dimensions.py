from datetime import datetime, timezone

from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint, MetricDataResult

def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = get_cloudwatch_client(region_name=config.get("region"))

    metric_queries = []
    for i, metric_filter in enumerate(payload["metric_filters"]):
        metric_queries.append({
            "Id": f"m{i}",
            "MetricStat": {
                "Metric": {
                    "Namespace": config["namespace"],
                    "MetricName": metric_filter["metric"],
                    "Dimensions": [{
                        "Name": k,
                        "Value": v
                    } for k, v in metric_filter.get("dimensions", {}).items()]
                },
                "Period": config.get("period_seconds", 60),
                "Stat": metric_filter.get("statistic", "Average"),
            },
            "ReturnData": True,
        })

    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
    )

    results = []
    for result in response["MetricDataResults"]:
        datapoints = []
        for i in range(len(result["Timestamps"])): # CloudWatch returns timestamps and values in separate lists
            datapoints.append(MetricDatapoint(timestamp=result["Timestamps"][i].timestamp(), value=float(result["Values"][i])))
        results.append(MetricDataResult(id=result["Id"], label=result["Label"], datapoints=sorted(datapoints, key=lambda p: p.timestamp)))
    
    return {"results": results}
