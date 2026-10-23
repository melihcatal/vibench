from datetime import datetime, timezone
from typing import Dict, Any, List

from observability_client import get_cloudwatch_client
from observability_models import AggregatedMetricStats

def aggregate_metric_stats(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, List[AggregatedMetricStats]]:
    config = config or {}
    client = get_cloudwatch_client(config.get("region"))

    statistics = payload.get("statistics", ["Average"])
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in config.get("dimensions", {}).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60),
        Statistics=statistics
    )

    aggregated_stats = []
    for dp in response["Datapoints"]:
        for stat in statistics:
            if stat in dp:
                aggregated_stats.append(AggregatedMetricStats(statistic_name=stat, value=float(dp[stat])))
    
    return {"aggregated_stats": aggregated_stats}
