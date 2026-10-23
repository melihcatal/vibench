"""Query metric data filtered by resource labels or dimensions.

Uses Google Cloud Monitoring (google-cloud-monitoring) to retrieve
metric time series that match specific resource label or metric label
filters, supporting equality, inequality, and regex match operators.

Required environment:
    GOOGLE_APPLICATION_CREDENTIALS - path to GCP service account JSON
    GCP_PROJECT or GOOGLE_CLOUD_PROJECT - GCP project ID
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from google.cloud import monitoring_v3

from observability_client import ObservabilityClient
from observability_models import DimensionFilter, MetricSeries


def parse_dimension_arg(dim_str: str) -> DimensionFilter:
    """Parse a dimension filter string like 'resource.label.zone=us-central1-a'.

    Supported operators: =, !=, =~, !=~
    """
    for op in ["!=~", "=~", "!=", "="]:
        if op in dim_str:
            name, value = dim_str.split(op, 1)
            return DimensionFilter(
                dimension_name=name.strip(),
                operator=op,
                value=value.strip(),
            )
    raise ValueError(f"Cannot parse dimension filter: {dim_str}")


def filter_metric_dimensions(
    metric_type: str,
    dimensions: List[DimensionFilter],
    project_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    minutes: int = 60,
) -> List[MetricSeries]:
    """Query metric data filtered by resource labels or dimensions.

    Args:
        metric_type: GCP metric type
        dimensions: List of DimensionFilter objects
        project_id: GCP project ID
        start_time: Window start
        end_time: Window end
        minutes: Lookback minutes

    Returns:
        List of MetricSeries matching all dimension filters.
    """
    client = ObservabilityClient(project_id=project_id)
    return client.filter_metric_dimensions(
        metric_type=metric_type,
        dimensions=dimensions,
        start_time=start_time,
        end_time=end_time,
        minutes=minutes,
    )


def format_filtered_series(series_list: List[MetricSeries]) -> str:
    """Format filtered series into readable JSON."""
    output = []
    for s in series_list:
        entry = {
            "metric_type": s.metric_type,
            "resource_type": s.resource_type,
            "resource_labels": s.resource_labels,
            "metric_labels": s.metric_labels,
            "point_count": len(s.points),
            "sample_values": [
                {"timestamp": p.timestamp.isoformat(), "value": p.value}
                for p in s.points[:5]
            ],
        }
        output.append(entry)
    return json.dumps(output, indent=2, default=str)


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter metric dimensions via Google Cloud Monitoring")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--dimension", action="append", required=True,
                        help="Dimension filter: name.operator=value")
    parser.add_argument("--start", default=None)
    parser.add_argument("--end", default=None)
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()

    dimensions = [parse_dimension_arg(d) for d in args.dimension]
    start = datetime.fromisoformat(args.start) if args.start else None
    end = datetime.fromisoformat(args.end) if args.end else None

    results = filter_metric_dimensions(
        metric_type=args.metric_type,
        dimensions=dimensions,
        project_id=args.project_id,
        start_time=start,
        end_time=end,
        minutes=args.minutes,
    )
    print(format_filtered_series(results))


if __name__ == "__main__":
    main()
