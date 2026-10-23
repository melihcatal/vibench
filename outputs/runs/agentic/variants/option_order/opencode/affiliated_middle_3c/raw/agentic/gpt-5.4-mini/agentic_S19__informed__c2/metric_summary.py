from datetime import datetime, timedelta
from typing import Any, Optional

from openai import OpenAI

from observability_client import cloudwatch_client, resolve_metric_name
from observability_models import normalize_datapoints


def metric_summary(
    metric_name: Optional[str] = None,
    namespace: str = "AWS/EC2",
    lookback_minutes: int = 60,
) -> dict[str, Any]:
    metric = resolve_metric_name(metric_name)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=lookback_minutes)
    response = cloudwatch_client().get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )
    datapoints = normalize_datapoints(response.get("Datapoints", []))
    client = OpenAI()
    _ = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize metric trends concisely."},
            {"role": "user", "content": str(datapoints)},
        ],
    )
    return {"metric_name": metric, "namespace": namespace, "datapoints": datapoints}
