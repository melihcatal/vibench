import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


class MetricSummaryError(Exception):
    pass


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _normalize_points(points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for point in points:
        timestamp = point.get("timestamp") or point.get("time") or point.get("ts")
        value = point.get("value")
        if timestamp is None or value is None:
            continue
        normalized.append({"timestamp": timestamp, "value": float(value)})
    return normalized


def _build_prompt(metric_name: str, points: List[Dict[str, Any]], context: Optional[str]) -> str:
    payload = {
        "metric_name": metric_name,
        "points": points,
        "context": context,
    }
    return (
        "Summarize recent metric trends or anomalies in concise JSON with keys "
        "summary, trend, anomalies, and recommendation. Use only the provided data.\n"
        + str(payload)
    )


def summarize_metric(metric_name: str, points: List[Dict[str, Any]], context: Optional[str] = None) -> Dict[str, Any]:
    normalized_points = _normalize_points(points)
    if not metric_name:
        raise MetricSummaryError("metric_name is required")
    if not normalized_points:
        raise MetricSummaryError("at least one datapoint is required")

    client = _client()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=_build_prompt(metric_name, normalized_points, context),
    )
    text = getattr(response, "output_text", None) or ""
    return {
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "metric_name": metric_name,
        "datapoint_count": len(normalized_points),
        "summary": text.strip(),
    }


def main() -> None:
    raise SystemExit("Import and call summarize_metric() from this module.")


if __name__ == "__main__":
    main()
