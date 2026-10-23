from __future__ import annotations

from typing import List

from google.cloud.monitoring_v3.types import ListTimeSeriesRequest

from observability_client import (
    build_monitoring_filter,
    monitoring_client,
    project_resource_name,
)
from observability_models import (
    MetricPoint,
    MetricSeriesResponse,
    MetricWindowRequest,
    normalize_labels,
    parse_float,
)


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    client = monitoring_client()
    pager = client.list_time_series(
        request={
            "name": project_resource_name(request.project_id),
            "filter": build_monitoring_filter(
                request.metric_type, request.filter_labels
            ),
            "interval": request.interval(),
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": {
                "alignment_period": {"seconds": request.alignment_period_seconds},
                "per_series_aligner": request.per_series_aligner,
            },
            "page_size": request.limit,
        }
    )

    points: List[MetricPoint] = []
    for series in pager:
        series_name = getattr(series.metric, "type", request.metric_type)
        labels = normalize_labels(dict(series.metric.labels))
        labels.update(
            {f"resource.{k}": str(v) for k, v in dict(series.resource.labels).items()}
        )
        for point in series.points:
            points.append(
                MetricPoint(
                    timestamp=point.interval.end_time.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    value=parse_float(
                        point.value._pb.ListFields()[0][1]
                        if point.value._pb.ListFields()
                        else None
                    ),
                    labels=labels,
                    resource_type=series.resource.type,
                    metric_kind=getattr(series, "metric_kind", None).name
                    if getattr(series, "metric_kind", None)
                    else None,
                    value_type=getattr(series, "value_type", None).name
                    if getattr(series, "value_type", None)
                    else None,
                    series_name=series_name,
                )
            )

    return MetricSeriesResponse(
        metric_type=request.metric_type,
        points=points,
        next_page_token=getattr(pager, "next_page_token", None),
    )
