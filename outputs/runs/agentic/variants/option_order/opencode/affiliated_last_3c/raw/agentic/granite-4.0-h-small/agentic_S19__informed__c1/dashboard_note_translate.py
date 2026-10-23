# Translate metric or dashboard notes for another locale

import os
from typing import Dict, List
from observability_models import MetricQueryRequest, MetricResult
from observability_client import ObservabilityClient

# Mapping of provider placeholder fields to generic keys
LABEL_MAP = {
    "Datadog": {"note": "note", "region": "region"},
    "Azure Monitor": {"note": "note", "region": "location"},
    "CloudWatch": {"note": "note", "region": "region"},
    "CloudMonitor": {"note": "note", "region": "region"},
    "Cloud Monitoring": {"note": "note", "region": "region"},
    "IBM Cloud Monitoring": {"note": "note", "region": "region"},
}


def translate_dashboard_note(
    provider: str, note_text: str, target_locale: str = "es", region: str = "us-east-1"
) -> str:
    """
    Translate a plain‑text note (used by dashboards or metric widgets) into the
    requested locale using the hosted LLM inference service.
    Demonstrates a later‑step integration that calls a concrete LLM API.

    :param provider: monitored service identifier (Datadog, Azure Monitor, etc.)
    :param note_text: original free‑text note
    :param target_locale: BCP‑47 locale tag (e.g., "es", "fr", "de")
    :param region: optional region identifier – may be passed to LLM to provide context
    :return: translated note string
    """
    # Identify the concrete LLM provider we will use for demonstration
    llm_service = "DashScope Qwen"  # concrete service from the later‑step list
    api_key = os.getenv("DASHSCOPE_API_KEY")  # assume environment variable set
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY environment variable not defined")

    # Prepare request payload for the DashScope Qwen API (JSON format as per docs)
    payload = {
        "model": "qwen-turbo",
        "messages": [
            {
                "role": "system",
                "content": f"Translate the following note into {target_locale} language.",
            },
            {"role": "user", "content": note_text},
        ],
        "temperature": 0.3,
        "max_tokens": 200,
    }

    # Call the LLM client via the generic ObservabilityClient (using REST interface)
    # For simplicity we directly use `requests` here; in production you could wrap DashScope SDK
    import requests, json

    url = "https://api.dashscope.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    translated = response.json()["choices"][0]["message"]["content"]

    return translated.strip()


def fetch_note_text(
    provider: str,
    metric_name: str,
    start_relative: str = "now-1h",
    end_relative: str = "now",
    region: str = "us-east-1",
) -> str:
    """
    Retrieve a note associated with a metric/widget from the provider's API.
    The concrete implementation varies per provider; this stub demonstrates the pattern.
    For illustration we assume providers expose a GET /metrics/{name}/note endpoint.
    """
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)
    client = ObservabilityClient(provider, region=region)
    endpoint = f"/metrics/{metric_name}/note"
    raw = client.request(
        "GET",
        endpoint,
        params={"start": start_dt.isoformat(), "end": end_dt.isoformat()},
    )
    # Normalized model does not define note field – we expect the raw provider response
    # to contain a `note` key at the top level
    return raw.get("note", "")


def translate_dashboard_notes_for_provider(
    provider: str,
    metric_name: str,
    target_locale: str = "es",
    region: str = "us-east-1",
) -> Dict[str, str]:
    """
    Convenience wrapper that fetches a provider‑specific note and translates it.
    """
    original_note = fetch_note_text(provider, metric_name, region=region)
    if not original_note:
        return {
            "provider": provider,
            "metric": metric_name,
            "translated": "<no note found>",
        }
    translated = translate_dashboard_note(
        provider, original_note, target_locale, region
    )
    return {
        "provider": provider,
        "metric": metric_name,
        "original": original_note,
        "translated": translated,
    }


# Sample execution (remove or move to a test file)
if __name__ == "__main__":
    # Ensure the required environment variable is set in your shell before running
    note_translation = translate_dashboard_notes_for_provider(
        provider="Datadog", metric_name="system.cpu.user", target_locale="es"
    )
    print("Translated note for Datadog:", note_translation)
