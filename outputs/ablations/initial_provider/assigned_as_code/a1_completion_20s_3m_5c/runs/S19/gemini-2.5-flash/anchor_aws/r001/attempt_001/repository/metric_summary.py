from datetime import datetime, timezone
from typing import Dict, Any
import statistics

from observability_client import CloudWatchClient

def metric_summary(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    client_wrapper = CloudWatchClient(region_name=config.get("region") if config else None)
    cloudwatch_config = client_wrapper.get_cloudwatch_config(config)
    client = client_wrapper.get_client()

    metric_data_queries = [{
        'Id': 'm1',
        'MetricStat': {
            'Metric': {
                'Namespace': cloudwatch_config["namespace"],
                'MetricName': payload["metric"],
                'Dimensions': [{'Name': k, 'Value': v} for k, v in cloudwatch_config.get("dimensions", {}).items() if v is not None]
            },
            'Period': cloudwatch_config.get("period_seconds", 60),
            'Stat': 'Average'
        },
        'Label': payload.get("label", "Metric Summary")
    }]

    response = client.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        ScanBy='TimestampAscending'
    )

    summary = {
        "metric_name": payload["metric"],
        "start_time": payload["start_time"],
        "end_time": payload["end_time"],
        "datapoint_count": 0,
        "average": None,
        "minimum": None,
        "maximum": None,
        "trend": "no data"
    }

    if response["MetricDataResults"] and response["MetricDataResults"][0]["Values"]:
        values = [float(v) for v in response["MetricDataResults"][0]["Values"]]
        if values:
            summary["datapoint_count"] = len(values)
            summary["average"] = statistics.mean(values)
            summary["minimum"] = min(values)
            summary["maximum"] = max(values)

            if len(values) > 1:
                # Simple trend analysis: compare first and last value
                if values[-1] > values[0]:
                    summary["trend"] = "increasing"
                elif values[-1] < values[0]:
                    summary["trend"] = "decreasing"
                else:
                    summary["trend"] = "stable"
            else:
                summary["trend"] = "stable (single datapoint)"

    return summary
