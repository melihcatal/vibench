"""Retrieve aggregated statistics for a metric over a time window.

Uses Google Cloud Monitoring (google-cloud-monitoring) to compute
aggregated metric statistics (mean, count, sum, min, max, percentiles)
over a specified time window with configurable alignment periods.

Required environment:
    GOOGLE_APPLICATION_CREDENTIALS - path to GCP service account JSON
    GCP_PROJECT or GOOGLE_CLOUD_PROJECT - GCP project ID
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Optional

from google.cloud import monitoring_v3

from observability_client import ObservabilityClient
from observability_models import AggregationKind, AggregationResult, AlignmentPeriod


def aggregate_metric_stats(
    metric_type: str,
    aggregation: AggregationKind = AggregationKind.AVERAGE,
    alignment: AlignmentPeriod = AlignmentPeriod.FIVE_MINUTES,
    project_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    filter_expression: Optional[str] = None,
    minutes: int = 60,
) -> AggregationResult:
    """Retrieve aggregated statistics for a metric over a time window.

    Args:
        metric_type: GCP metric type
        aggregation: AggregationKind (MEAN, COUNT, SUM, MIN, MAX, etc.)
        alignment: AlignmentPeriod for bucketing datapoints
        project_id: GCP project ID
        start_time: Window start
        end_time: Window end
        filter_expression: Additional GCM filter
        minutes: Lookback minutes

    Returns:
        AggregationResult with per-series aggregated datapoints and summary stats.
    """
    client = ObservabilityClient(project_id=project_id)
    return client.aggregate_metric_stats(
        metric_type=metric_type,
        aggregation=aggregation,
        alignment=alignment,
        start_time=start_time,
        end_time=end_time,
        filter_expression=filter_expression,
        minutes=minutes,
    )


def format_aggregation(result: AggregationResult) -> str:
    """Format aggregation result as JSON."""
    output = {
        "metric_type": result.metric_type,
        "aggregation": result.aggregation.value,
        "alignment_period": result.alignment_period.value,
        "summary": result.summary,
        "series": [
            {
                "metric_type": s.metric_type,
                "resource_type": s.resource_type,
                "resource_labels": s.resource_labels,
                "point_count": len(s.points),
                "points": [
                    {"timestamp": p.timestamp.isoformat(), "value": p.value}
                    for p in s.points
                ],
            }
            for s in result.series
        ],
    }
    return json.dumps(output, indent=2, default=str)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate metric stats via Google Cloud Monitoring")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--aggregation", default="AGGREGATION_MEAN",
                        choices=[k.value for k in AggregationKind])
    parser.add_argument("--alignment", default="300s",
                        choices=[v.value for v in AlignmentPeriod])
    parser.add_argument("--start", default=None)
    parser.add_argument("--end", default=None)
    parser.add_argument("--filter", default=None)
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()

    agg = AggregationKind(args.aggregation)
    align = AlignmentPeriod(args.alignment)
    start = datetime.fromisoformat(args.start) if args.start else None
    end = datetime.fromisoformat(args.end) if args.end else None

    result = aggregate_metric_stats(
        metric_type=args.metric_type,
        aggregation=agg,
        alignment=align,
        project_id=args.project_id,
        start_time=start,
        end_time=end,
        filter_expression=args.filter,
        minutes=args.minutes,
    )
    print(format_aggregation(result))


if __name__ == "__main__":
    main()
