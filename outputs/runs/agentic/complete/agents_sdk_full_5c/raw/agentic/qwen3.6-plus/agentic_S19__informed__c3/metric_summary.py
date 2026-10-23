"""Summarize recent metric trends or anomalies.

Uses Anthropic Messages API (anthropic SDK) with Claude 3.5 Sonnet
to analyze metric datapoints and produce a natural-language summary
of trends, anomalies, and notable patterns.

Required environment:
    ANTHROPIC_API_KEY - Anthropic API key
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from anthropic import Anthropic

from observability_client import ObservabilityClient
from observability_models import AggregationKind, AlignmentPeriod, MetricSeries

ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def build_metric_prompt(
    metric_type: str,
    series_list: List[MetricSeries],
    summary_stats: Optional[Dict[str, float]] = None,
) -> str:
    """Build a prompt for Anthropic Claude to summarize metric trends."""
    lines = [
        f"You are an observability analyst. Summarize the trends and any anomalies for the metric: {metric_type}",
        "",
        "Datapoints per series:",
    ]

    for i, s in enumerate(series_list):
        lines.append(f"\nSeries {i + 1}:")
        lines.append(f"  Resource: {s.resource_type} labels={s.resource_labels}")
        lines.append(f"  Metric labels: {s.metric_labels}")
        lines.append(f"  Points ({len(s.points)}):")
        for p in s.points[:20]:
            lines.append(f"    {p.timestamp.isoformat()}: {p.value}")

    if summary_stats:
        lines.append("\nAggregate statistics:")
        for k, v in summary_stats.items():
            lines.append(f"  {k}: {v}")

    lines.append(
        "\nPlease provide:"
        "\n1. A brief overview of the metric behavior"
        "\n2. Any detected anomalies or unusual patterns"
        "\n3. Possible causes and recommendations"
    )
    return "\n".join(lines)


def summarize_metric_trends(
    metric_type: str,
    project_id: Optional[str] = None,
    minutes: int = 60,
    aggregation: AggregationKind = AggregationKind.AVERAGE,
    alignment: AlignmentPeriod = AlignmentPeriod.FIVE_MINUTES,
    anthropic_api_key: Optional[str] = None,
) -> str:
    """Summarize recent metric trends using Anthropic Claude.

    Retrieves aggregated metric data from Google Cloud Monitoring,
    then sends it to Anthropic's Claude 3.5 Sonnet for analysis.
    """
    api_key = anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY must be set")

    client = Anthropic(api_key=api_key)

    obs_client = ObservabilityClient(project_id=project_id)
    agg_result = obs_client.aggregate_metric_stats(
        metric_type=metric_type,
        aggregation=aggregation,
        alignment=alignment,
        minutes=minutes,
    )

    prompt = build_metric_prompt(metric_type, agg_result.series, agg_result.summary)

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=2048,
        system="You are an expert SRE and observability engineer. Provide concise, actionable summaries of metric data.",
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text if message.content else ""


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize metric trends via Anthropic Claude")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--minutes", type=int, default=60)
    parser.add_argument("--aggregation", default="AGGREGATION_MEAN",
                        choices=[k.value for k in AggregationKind])
    parser.add_argument("--alignment", default="300s",
                        choices=[v.value for v in AlignmentPeriod])
    args = parser.parse_args()

    agg = AggregationKind(args.aggregation)
    align = AlignmentPeriod(args.alignment)

    summary = summarize_metric_trends(
        metric_type=args.metric_type,
        project_id=args.project_id,
        minutes=args.minutes,
        aggregation=agg,
        alignment=align,
    )
    print(summary)


if __name__ == "__main__":
    main()
