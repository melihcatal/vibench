from datetime import datetime, timezone
from typing import List, Dict, Any

from observability_client import CloudWatchClient
from observability_models import MetricDataResult, MetricDatapoint

def filter_metric_dimensions(payload: Dict[str, Any], config: Dict[str, Any] = None) -> List[MetricDataResult]:
    client_wrapper = CloudWatchClient(region_name=config.get("region") if config else None)
    cloudwatch_config = client_wrapper.get_cloudwatch_config(config)
    client = client_wrapper.get_client()

    metric_data_queries = []
    for i, dimension_filter in enumerate(payload.get("dimension_filters", [])):
        dimensions = [{'Name': k, 'Value': v} for k, v in dimension_filter.get("dimensions", {}).items()]
        metric_data_queries.append({
            'Id': f'm{i}',
            'MetricStat': {
                'Metric': {
                    'Namespace': cloudwatch_config["namespace"],
                    'MetricName': payload["metric"],
                    'Dimensions': dimensions
                },
                'Period': cloudwatch_config.get("period_seconds", 60),
                'Stat': payload.get("statistic", "Average")
            },
            'Label': dimension_filter.get("label", f"Series {i}")
        })

    if not metric_data_queries:
        # If no dimension_filters are provided, query the metric without specific dimensions
        metric_data_queries.append({
            'Id': 'm0',
            'MetricStat': {
                'Metric': {
                    'Namespace': cloudwatch_config["namespace"],
                    'MetricName': payload["metric"],
                    'Dimensions': [{'Name': k, 'Value': v} for k, v in cloudwatch_config.get("dimensions", {}).items() if v is not None]
                },
                'Period': cloudwatch_config.get("period_seconds", 60),
                'Stat': payload.get("statistic", "Average")
            },
            'Label': 'Overall Series'
        })

    response = client.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        ScanBy='TimestampAscending'
    )

    results = []
    for result in response["MetricDataResults"]:
        datapoints = []
        # CloudWatch returns Timestamps and Values as separate lists, need to combine them
        for i in range(len(result.get("Timestamps", []))):
            datapoints.append(MetricDatapoint(
                timestamp=result["Timestamps"][i].timestamp(),
                value=float(result["Values"][i])
            ))
        results.append(MetricDataResult(
            label=result.get("Label", result["Id"]),
            datapoints=sorted(datapoints, key=lambda p: p.timestamp)
        ))
    return results
