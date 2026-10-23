from datetime import datetime, timezone

from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint, MetricDataResult

def compare_metric_series(payload, config=None):
    config = config or {}
    client = get_cloudwatch_client(region_name=config.get("region"))

    metric_queries = []

    # First series
    metric_queries.append({
        "Id": "series1",
        "MetricStat": {
            "Metric": {
                "Namespace": config["namespace"],
                "MetricName": payload["series1"]["metric"],
                "Dimensions": [{
                    "Name": k,
                    "Value": v
                } for k, v in payload["series1"].get("dimensions", {}).items()]
            },
            "Period": config.get("period_seconds", 60),
            "Stat": payload["series1"].get("statistic", "Average"),
        },
        "ReturnData": True,
    })

    # Second series
    metric_queries.append({
        "Id": "series2",
        "MetricStat": {
            "Metric": {
                "Namespace": config["namespace"],
                "MetricName": payload["series2"]["metric"],
                "Dimensions": [{
                    "Name": k,
                    "Value": v
                } for k, v in payload["series2"].get("dimensions", {}).items()]
            },
            "Period": config.get("period_seconds", 60),
            "Stat": payload["series2"].get("statistic", "Average"),
        },
        "ReturnData": True,
    })

    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
    )

    results = {}
    for result in response["MetricDataResults"]:
        datapoints = []
        for i in range(len(result["Timestamps"])): # CloudWatch returns timestamps and values in separate lists
            datapoints.append(MetricDatapoint(timestamp=result["Timestamps"][i].timestamp(), value=float(result["Values"][i])))
        results[result["Id"]] = MetricDataResult(id=result["Id"], label=result["Label"], datapoints=sorted(datapoints, key=lambda p: p.timestamp))
    
    return {"comparison_results": results}
