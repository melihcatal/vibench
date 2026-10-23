from observability_client import load_config, cloudwatch_client
from observability_models import summarize_series


def metric_summary(payload, config=None):
    cfg = load_config(config)
    client = cloudwatch_client(config)
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": cfg.namespace,
                        "MetricName": payload["metric"],
                        "Dimensions": [{"Name": k, "Value": v} for k, v in cfg.dimensions.items()],
                    },
                    "Period": cfg.period_seconds,
                    "Stat": "Average",
                },
                "ReturnData": True,
            }
        ],
        StartTime=payload["start_time"],
        EndTime=payload["end_time"],
    )
    values = response.get("MetricDataResults", [{}])[0]
    points = [{"timestamp": t, "value": v} for t, v in zip(values.get("Timestamps", []), values.get("Values", []))]
    summary = summarize_series(points)
    summary["metric"] = payload["metric"]
    return summary
