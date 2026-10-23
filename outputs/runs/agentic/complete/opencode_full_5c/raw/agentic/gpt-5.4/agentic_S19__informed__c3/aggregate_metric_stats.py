from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import get_cloudwatch_client
from observability_models import (
    AggregateStatsResponse,
    MetricWindowRequest,
    isoformat_utc,
    normalize_dimensions,
)


def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    dimensions: Optional[Dict[str, Any]] = None,
    unit: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    request = MetricWindowRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        stat="Average",
        unit=unit,
        dimensions=normalize_dimensions(dimensions),
    )
    client = get_cloudwatch_client(region_name=region_name)
    response = client.client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=["Minimum", "Maximum", "Average", "Sum", "SampleCount"],
        Dimensions=request.cloudwatch_dimensions(),
        **({"Unit": request.unit} if request.unit else {}),
    )
    datapoints = sorted(
        response.get("Datapoints", []), key=lambda item: item["Timestamp"]
    )
    if not datapoints:
        aggregate = AggregateStatsResponse(
            provider=client.provider,
            namespace=request.namespace,
            metric_name=request.metric_name,
            start_time=isoformat_utc(request.start_time),
            end_time=isoformat_utc(request.end_time),
            sample_count=0,
            minimum=None,
            maximum=None,
            average=None,
            sum=None,
            unit=request.unit,
            dimensions=request.dimensions,
        )
        return asdict(aggregate)
    sample_count = int(sum(item.get("SampleCount", 0) for item in datapoints))
    sum_value = float(sum(item.get("Sum", 0.0) for item in datapoints))
    min_candidates = [
        float(item["Minimum"]) for item in datapoints if "Minimum" in item
    ]
    max_candidates = [
        float(item["Maximum"]) for item in datapoints if "Maximum" in item
    ]
    average = sum_value / sample_count if sample_count else None
    aggregate = AggregateStatsResponse(
        provider=client.provider,
        namespace=request.namespace,
        metric_name=request.metric_name,
        start_time=isoformat_utc(request.start_time),
        end_time=isoformat_utc(request.end_time),
        sample_count=sample_count,
        minimum=min(min_candidates) if min_candidates else None,
        maximum=max(max_candidates) if max_candidates else None,
        average=average,
        sum=sum_value,
        unit=datapoints[-1].get("Unit") or request.unit,
        dimensions=request.dimensions,
    )
    return asdict(aggregate)
