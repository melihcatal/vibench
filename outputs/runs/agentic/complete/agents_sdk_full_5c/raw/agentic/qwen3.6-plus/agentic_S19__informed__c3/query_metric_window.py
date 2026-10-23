"""Query recent datapoints for a named metric over a time window.

Uses Google Cloud Monitoring (google-cloud-monitoring) to retrieve
full time-series data for a specified metric type within a given time window.

Required environment:
    GOOGLE_APPLICATION_CREDENTIALS - path to GCP service account JSON
    GCP_PROJECT or GOOGLE_CLOUD_PROJECT - GCP project ID
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import List, Optional

from google.cloud import monitoring_v3

from observability_client import ObservabilityClient, project_name
from observability_models import MetricDataPoint, MetricSeries


def query_metric_window(
    metric_type: str,
    project_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    filter_expression: Optional[str] = None,
    minutes: int = 60,
) -> List[MetricSeries]:
    """Query recent datapoints for a named metric over a time window.

    Args:
        metric_type: Google Cloud Monitoring metric type, e.g.
            "compute.googleapis.com/instance/cpu/utilization"
        project_id: GCP project ID (falls back to env vars)
        start_time: Window start (UTC)
        end_time: Window end (UTC)
        filter_expression: Additional GCM filter string
        minutes: Lookback minutes when start/end not provided

    Returns:
        List of MetricSeries containing datapoints for the metric.
    """
    client = ObservabilityClient(project_id=project_id)
    return client.query_metric_window(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        filter_expression=filter_expression,
        minutes=minutes,
    )


def format_series(series_list: List[MetricSeries]) -> str:
    """Format metric series into a readable JSON string."""
    output = []
    for s in series_list:
        entry = {
            "metric_type": s.metric_type,
            "resource_type": s.resource_type,
            "resource_labels": s.resource_labels,
            "metric_labels": s.metric_labels,
            "point_count": len(s.points),
            "points": [
                {
                    "timestamp": p.timestamp.isoformat(),
                    "value": p.value,
                    "labels": p.labels,
                }
                for p in s.points
            ],
        }
        output.append(entry)
    return json.dumps(output, indent=2, default=str)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query metric window via Google Cloud Monitoring")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None, help="GCP project ID")
    parser.add_argument("--start", default=None, help="Start time ISO format")
    parser.add_argument("--end", default=None, help="End time ISO format")
    parser.add_argument("--filter", default=None, help="Additional filter expression")
    parser.add_argument("--minutes", type=int, default=60, help="Lookback window in minutes")
    args = parser.parse_args()

    start = datetime.fromisoformat(args.start) if args.start else None
    end = datetime.fromisoformat(args.end) if args.end else None

    results = query_metric_window(
        metric_type=args.metric_type,
        project_id=args.project_id,
        start_time=start,
        end_time=end,
        filter_expression=args.filter,
        minutes=args.minutes,
    )
    print(format_series(results))


if __name__ == "__main__":
    main()
