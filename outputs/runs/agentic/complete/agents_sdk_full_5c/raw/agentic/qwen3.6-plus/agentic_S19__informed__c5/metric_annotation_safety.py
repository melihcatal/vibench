"""
metric_annotation_safety.py - Check free-text metric labels or annotations for unsafe text.
Uses Azure AI Content Safety service for text moderation.
Provider: Azure AI Content Safety
SDK: requests (REST interface to contentsafety.azure.com)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests

from observability_client import (
    DatadogConfig,
    DatadogMetricsClient,
    build_windowed_request,
)


CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_annotation_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check free-text metric labels or annotations for unsafe content
    using Azure AI Content Safety.

    Analyzes text for categories including hate, self-harm, sexual, and violence.

    Args:
        text: The annotation or label text to analyze.
        endpoint: Azure Content Safety endpoint URL. Falls back to
                  AZURE_CONTENT_SAFETY_ENDPOINT env var.
        api_key: Azure Content Safety API key. Falls back to
                 AZURE_CONTENT_SAFETY_KEY env var.

    Returns:
        Dict with safety analysis results per category.
    """
    endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )
    if not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required"
        )

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze"
    params = {"api-version": CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        params=params,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    return data


def check_metric_annotations_safety(
    metric_name: str,
    window_minutes: int = 60,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve metric annotations from Datadog and check each for unsafe content.

    Queries Datadog for the metric, extracts scope and display names which may
    contain user-provided annotations, then runs Azure AI Content Safety
    analysis on each text field.

    Args:
        metric_name: The Datadog metric identifier.
        window_minutes: Time window in minutes.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.

    Returns:
        List of dicts with annotation text and safety results.
    """
    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request = build_windowed_request(
        metric_name=metric_name,
        window_minutes=window_minutes,
        aggregation="avg",
        rollup=60,
    )

    response = client.query(request)

    results: List[Dict[str, Any]] = []

    for series in response.series:
        text_fields = []
        if series.scope:
            text_fields.append(("scope", series.scope))
        if series.display_name and series.display_name != series.metric_name:
            text_fields.append(("display_name", series.display_name))

        for field_name, text in text_fields:
            try:
                safety_result = check_annotation_safety(text, endpoint, api_key)
                results.append({
                    "metric": metric_name,
                    "field": field_name,
                    "text": text,
                    "safety_analysis": safety_result,
                    "status": "analyzed",
                })
            except requests.HTTPError as exc:
                results.append({
                    "metric": metric_name,
                    "field": field_name,
                    "text": text,
                    "status": "error",
                    "error": str(exc),
                })

    return results


def summarize_safety_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize safety check results, flagging any flagged categories."""
    summary: Dict[str, Any] = {
        "total_checked": len(results),
        "flagged": 0,
        "clean": 0,
        "errors": 0,
        "details": [],
    }

    for result in results:
        if result["status"] == "error":
            summary["errors"] += 1
            summary["details"].append(result)
            continue

        analysis = result.get("safety_analysis", {})
        categories = analysis.get("categoriesAnalysis", [])

        is_flagged = False
        flagged_categories = []
        for cat in categories:
            severity = cat.get("severity", 0)
            if severity and severity > 0:
                is_flagged = True
                flagged_categories.append({
                    "category": cat.get("category"),
                    "severity": severity,
                })

        if is_flagged:
            summary["flagged"] += 1
            result["flagged"] = True
            result["flagged_categories"] = flagged_categories
        else:
            summary["clean"] += 1
            result["flagged"] = False

        summary["details"].append(result)

    return summary


def main():
    if len(sys.argv) < 2:
        print("Usage: metric_annotation_safety.py <metric_name> [--window MINUTES]")
        sys.exit(1)

    metric_name = sys.argv[1]
    window = 60

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--window" and i + 1 < len(sys.argv):
            window = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    results = check_metric_annotations_safety(metric_name, window)
    summary = summarize_safety_results(results)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
