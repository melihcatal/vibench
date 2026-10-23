"""Compare metric values for two resources or dimension filters over the same window.

Uses Google Cloud Monitoring (google-cloud-monitoring) to retrieve
two metric time series and compute delta statistics (mean, max, min)
and Pearson correlation between them.

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
from observability_models import MetricComparisonResult


def compare_metric_series(
    metric_type: str,
    filter_a: Optional[str] = None,
    filter_b: Optional[str] = None,
    project_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    minutes: int = 60,
) -> MetricComparisonResult:
    """Compare metric values for two resources or dimension filters.

    Args:
        metric_type: GCP metric type to compare
        filter_a: Filter expression for series A (e.g. resource labels)
        filter_b: Filter expression for series B
        project_id: GCP project ID
        start_time: Window start
        end_time: Window end
        minutes: Lookback minutes

    Returns:
        MetricComparisonResult with delta stats and correlation.
    """
    client = ObservabilityClient(project_id=project_id)
    return client.compare_metric_series(
        metric_type=metric_type,
        filter_a=filter_a,
        filter_b=filter_b,
        start_time=start_time,
        end_time=end_time,
        minutes=minutes,
    )


def format_comparison(result: MetricComparisonResult) -> str:
    """Format comparison result as JSON."""
    output = {
        "delta_mean": result.delta_mean,
        "delta_max": result.delta_max,
        "delta_min": result.delta_min,
        "correlation": result.correlation,
        "series_a": {
            "metric_type": result.series_a.metric_type,
            "resource_type": result.series_a.resource_type,
            "resource_labels": result.series_a.resource_labels,
            "point_count": len(result.series_a.points),
            "points": [
                {"timestamp": p.timestamp.isoformat(), "value": p.value}
                for p in result.series_a.points[:10]
            ],
        },
        "series_b": {
            "metric_type": result.series_b.metric_type,
            "resource_type": result.series_b.resource_type,
            "resource_labels": result.series_b.resource_labels,
            "point_count": len(result.series_b.points),
            "points": [
                {"timestamp": p.timestamp.isoformat(), "value": p.value}
                for p in result.series_b.points[:10]
            ],
        },
    }
    return json.dumps(output, indent=2, default=str)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare metric series via Google Cloud Monitoring")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--filter-a", default=None, help="Filter for series A")
    parser.add_argument("--filter-b", default=None, help="Filter for series B")
    parser.add_argument("--start", default=None)
    parser.add_argument("--end", default=None)
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()

    start = datetime.fromisoformat(args.start) if args.start else None
    end = datetime.fromisoformat(args.end) if args.end else None

    result = compare_metric_series(
        metric_type=args.metric_type,
        filter_a=args.filter_a,
        filter_b=args.filter_b,
        project_id=args.project_id,
        start_time=start,
        end_time=end,
        minutes=args.minutes,
    )
    print(format_comparison(result))


if __name__ == "__main__":
    main()
