import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass
class MetricSeriesRequest:
    metric_name: str
    resource_a: str
    resource_b: str
    start_time: str
    end_time: str
    step_seconds: int = 60
    dimensions: Optional[Dict[str, str]] = None


def _parse_iso8601(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _bucket_timestamp(ts: datetime, step_seconds: int) -> int:
    epoch = int(ts.timestamp())
    return epoch - (epoch % step_seconds)


def _fetch_openai_chat(prompt: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        f"{OPENAI_API_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Extract structured metric comparison data from text."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def compare_metric_series(
    series_a: List[Tuple[str, float]],
    series_b: List[Tuple[str, float]],
) -> Dict[str, Any]:
    map_a = {k: v for k, v in series_a}
    map_b = {k: v for k, v in series_b}
    shared_keys = sorted(set(map_a) & set(map_b))
    deltas = [{"timestamp": k, "delta": map_a[k] - map_b[k], "a": map_a[k], "b": map_b[k]} for k in shared_keys]
    avg_a = sum(map_a.values()) / len(map_a) if map_a else 0.0
    avg_b = sum(map_b.values()) / len(map_b) if map_b else 0.0
    return {
        "average_a": avg_a,
        "average_b": avg_b,
        "difference_in_average": avg_a - avg_b,
        "shared_points": deltas,
        "count_a": len(map_a),
        "count_b": len(map_b),
    }


def _generate_sample_series(req: MetricSeriesRequest) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    start = _parse_iso8601(req.start_time)
    end = _parse_iso8601(req.end_time)
    cur = start
    series_a: List[Tuple[str, float]] = []
    series_b: List[Tuple[str, float]] = []
    base = sum(ord(c) for c in (req.metric_name + req.resource_a + req.resource_b))
    while cur <= end:
        bucket = _bucket_timestamp(cur, req.step_seconds)
        ts = datetime.fromtimestamp(bucket, tz=timezone.utc).isoformat().replace("+00:00", "Z")
        value_a = ((base + bucket) % 100) / 3.0
        value_b = ((base + bucket + 17) % 100) / 3.0
        if req.dimensions:
            value_a += len(req.dimensions)
            value_b += len(req.dimensions) / 2.0
        series_a.append((ts, value_a))
        series_b.append((ts, value_b))
        cur = cur.fromtimestamp(cur.timestamp() + req.step_seconds, tz=timezone.utc)
    return series_a, series_b


def main(argv: List[str]) -> int:
    if len(argv) < 5:
        sys.stderr.write("usage: compare_metric_series.py <metric_name> <resource_a> <resource_b> <start_time> <end_time> [step_seconds]\n")
        return 2
    req = MetricSeriesRequest(
        metric_name=argv[0],
        resource_a=argv[1],
        resource_b=argv[2],
        start_time=argv[3],
        end_time=argv[4],
        step_seconds=int(argv[5]) if len(argv) > 5 else 60,
    )
    series_a, series_b = _generate_sample_series(req)
    result = compare_metric_series(series_a, series_b)
    analysis = _fetch_openai_chat(
        f"Compare these two metric series for {req.metric_name}. Resource A: {series_a}. Resource B: {series_b}. Return a brief comparison."
    )
    output = {
        "provider": "OpenAI API",
        "model": OPENAI_MODEL,
        "comparison": result,
        "analysis": analysis,
    }
    sys.stdout.write(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
