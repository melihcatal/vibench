from __future__ import annotations

from typing import Dict, Optional

from observability_client import build_metric_params, get_cloudwatch_client, load_metric_window
from observability_models import AggregatedMetricStats


def aggregate_metric_stats(
    metric_name: str,
    namespace: str,
    minutes: int = 60,
    period: int = 300,
    dimensions: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> AggregatedMetricStats:
    client = get_cloudwatch_client(region_name=region_name)
    query = load_metric_window(
        metric_name=metric_name,
        namespace=namespace,
        minutes=minutes,
        period=period,
        stat="Average",
        dimensions=dimensions,
    )
    params = build_metric_params(query)
    params["Statistics"] = ["Minimum", "Maximum", "Average", "Sum", "SampleCount"]
    response = client.get_metric_statistics(**params)
    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return AggregatedMetricStats(
            metric_name=metric_name,
            namespace=namespace,
            stat="multi",
            sample_count=0,
            minimum=None,
            maximum=None,
            average=None,
            sum=None,
            unit=None,
        )
    mins = [float(d["Minimum"]) for d in datapoints if "Minimum" in d]
    maxs = [float(d["Maximum"]) for d in datapoints if "Maximum" in d]
    avgs = [float(d["Average"]) for d in datapoints if "Average" in d]
    sums = [float(d["Sum"]) for d in datapoints if "Sum" in d]
    counts = [float(d["SampleCount"]) for d in datapoints if "SampleCount" in d]
    weighted_average = (sum(a * c for a, c in zip(avgs, counts)) / sum(counts)) if avgs and counts and sum(counts) else None
    return AggregatedMetricStats(
        metric_name=metric_name,
        namespace=namespace,
        stat="multi",
        sample_count=int(sum(counts)) if counts else 0,
        minimum=min(mins) if mins else None,
        maximum=max(maxs) if maxs else None,
        average=weighted_average,
        sum=sum(sums) if sums else None,
        unit=datapoints[0].get("Unit"),
    )
