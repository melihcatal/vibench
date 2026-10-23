import os
from datetime import datetime, timedelta, timezone

import requests


OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _window_bounds(minutes: int):
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return start, end


def _fetch_metric_series(metric_name: str, minutes: int, resource: str | None = None):
    base_url = os.getenv("METRICS_API_URL", "https://api.openai.com/v1")
    params = {"metric_name": metric_name, "minutes": str(minutes)}
    if resource:
        params["resource"] = resource
    response = requests.get(
        f"{base_url.rstrip('/')}/metrics/series",
        params=params,
        headers={"Authorization": f"Bearer {os.environ['METRICS_API_KEY']}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _summarize_series_with_openai(metric_name: str, series_payload: dict, start: datetime, end: datetime):
    prompt = (
        f"Summarize recent trends or anomalies for metric '{metric_name}' over the window "
        f"{start.isoformat()} to {end.isoformat()}. "
        f"Use the following metric payload as source data: {series_payload}."
    )
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize metric trends and anomalies concisely."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def metric_summary(metric_name: str, minutes: int = 60, resource: str | None = None):
    start, end = _window_bounds(minutes)
    series = _fetch_metric_series(metric_name, minutes, resource=resource)
    summary = _summarize_series_with_openai(metric_name, series, start, end)
    return {
        "metric_name": metric_name,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "summary": summary,
        "source": "OpenAI API",
    }
