from datetime import datetime, timezone
from typing import List, Dict, Any

from observability_client import CloudWatchClient
from observability_models import MetricDataResult, MetricDatapoint

def compare_metric_series(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, List[MetricDataResult]]:
    client_wrapper = CloudWatchClient(region_name=config.get("region") if config else None)
    cloudwatch_config = client_wrapper.get_cloudwatch_config(config)
    client = client_wrapper.get_client()

    metric_data_queries = []

    # Series 1
    dimensions_1 = [{'Name': k, 'Value': v} for k, v in payload["series_1_dimensions"].items()]
    metric_data_queries.append({
        'Id': 'series1',
        'MetricStat': {
            'Metric': {
                'Namespace': cloudwatch_config["namespace"],
                'MetricName': payload["metric"],
                'Dimensions': dimensions_1
            },
            'Period': cloudwatch_config.get("period_seconds", 60),
            'Stat': payload.get("statistic", "Average")
        },
        'Label': payload.get("series_1_label", "Series 1")
    })

    # Series 2
    dimensions_2 = [{'Name': k, 'Value': v} for k, v in payload["series_2_dimensions"].items()]
    metric_data_queries.append({
        'Id': 'series2',
        'MetricStat': {
            'Metric': {
                'Namespace': cloudwatch_config["namespace"],
                'MetricName': payload["metric"],
                'Dimensions': dimensions_2
            },
            'Period': cloudwatch_config.get("period_seconds", 60),
            'Stat': payload.get("statistic", "Average")
        },
        'Label': payload.get("series_2_label", "Series 2")
    })

    response = client.get_metric_data(
        MetricDataQueries=metric_data_queries,
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        ScanBy='TimestampAscending'
    )

    results = {"series_1": [], "series_2": []}
    for result in response["MetricDataResults"]:
        datapoints = []
        for i in range(len(result.get("Timestamps", []))):
            datapoints.append(MetricDatapoint(
                timestamp=result["Timestamps"][i].timestamp(),
                value=float(result["Values"][i])
            ))
        metric_data_result = MetricDataResult(
            label=result.get("Label", result["Id"]),
            datapoints=sorted(datapoints, key=lambda p: p.timestamp)
        )

        if result["Id"] == "series1":
            results["series_1"].append(metric_data_result)
        elif result["Id"] == "series2":
            results["series_2"].append(metric_data_result)

    return results
