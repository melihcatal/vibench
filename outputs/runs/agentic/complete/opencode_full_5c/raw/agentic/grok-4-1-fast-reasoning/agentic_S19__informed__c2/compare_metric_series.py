from datetime import datetime
from typing import List, Dict, Any
import boto3
from observability_client import create_aws_session
from observability_models import normalize_datapoints


def compare_metric_series(
    metric_name: str,
    dimensions1: List[Dict[str, str]],
    dimensions2: List[Dict[str, str]],
    start_time: datetime,
    end_time: datetime,
    namespace: str = "AWS/EC2",
    period_seconds: int = 300,
) -> Dict[str, Any]:
    session = create_aws_session()
    client = session.client("cloudwatch")

    def _query_dps(dim_filters: List[Dict[str, str]]):
        dims = [{"Name": f["Name"], "Value": f["Value"]} for f in dim_filters]
        resp = client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dims,
            StartTime=start_time,
            EndTime=end_time,
            Period=period_seconds,
            Statistics=["Average"],
        )
        return normalize_datapoints(resp["Datapoints"])

    dps1 = _query_dps(dimensions1)
    dps2 = _query_dps(dimensions2)

    avg1 = sum(d["value"] for d in dps1) / len(dps1) if dps1 else 0.0
    avg2 = sum(d["value"] for d in dps2) / len(dps2) if dps2 else 0.0

    return {
        "series1": {"avg": avg1, "datapoints": dps1},
        "series2": {"avg": avg2, "datapoints": dps2},
        "comparison": {
            "difference": avg1 - avg2,
            "ratio": avg1 / avg2 if avg2 != 0 else float("inf"),
        },
    }
