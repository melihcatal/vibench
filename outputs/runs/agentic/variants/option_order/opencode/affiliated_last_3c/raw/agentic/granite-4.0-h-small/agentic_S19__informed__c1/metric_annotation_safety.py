# Inspect free‑text metric labels/annotations for unsafe content

from typing import List, Dict
from observability_models import (
    MetricQueryRequest,
    MetricResult,
    normalize_metric_response,
)
from observability_client import ObservabilityClient

# Simple keyword sets that indicate potentially unsafe statements
PROHIBITED_TERMS = [
    "vuln",
    "exploit",
    "password",
    "secret",
    "credential",
    "key",
    "private",
    "unencrypted",
]
SUSPICIOUS_TERMS = ["fallback", "hardcoded", "deprecated", "legacy", "mock"]


def check_annotation_safety(
    provider: str,
    metric_name: str,
    start_relative: str = "now-1h",
    end_relative: str = "now",
    region: str = "us-east-1",
) -> Dict[str, List[str]]:
    """
    Pull recent datapoints, inspect any associated labels/annotations (free‑text fields),
    and return a list of detected unsafe words/phrases.

    Note: Not every provider returns textual annotations with the metric series. This
    implementation assumes that any label named `annotation` or `description` can contain
    free text. If absent, the function returns an empty unsafe list.

    :param provider: monitored service identifier (Datadog, Azure Monitor, CloudWatch, etc.)
    :param metric_name: metric identifier as understood by the provider
    :param start_relative: relative start token (default "now-1h")
    :param end_relative: relative end token (default "now")
    :param region: optional region/tenant identifier
    :return: dict with keys `unsafe` and `suspicious` containing detected term occurrences
    """
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)

    request = MetricQueryRequest(
        metric_name, start_dt.isoformat(), end_dt.isoformat(), limit=100
    )
    client = ObservabilityClient(provider, region=region)
    endpoint = "/query?from={}&to={}&limit=100".format(
        int(start_dt.timestamp()), int(end_dt.timestamp())
    )
    raw = client.request("GET", endpoint, params={"metric": metric_name})
    resp = normalize_metric_response(provider, raw)
    # Expect provider to expose dimensions/labels at the top level or inside each series
    labels = resp.metadata.get("labels", [])
    # Some services store a common description in metadata
    description = resp.metadata.get("description", "")

    text_blocks = labels + [description]

    # Flatten list of dicts if needed (some back‑ends return list of {key:value})
    def flatten(blocks):
        texts = []
        for b in blocks:
            if isinstance(b, dict):
                texts.extend(b.values())
            else:
                texts.append(str(b))
        return texts

    texts = flatten(text_blocks)

    unsafe = []
    suspicious = []
    lower_texts = [t.lower() for t in texts if t]
    for term in PROHIBITED_TERMS:
        if any(term in txt for txt in lower_texts):
            unsafe.append(term)
    for term in SUSPICIOUS_TERMS:
        if any(term in txt for txt in lower_texts):
            suspicious.append(term)

    return {
        "provider": provider,
        "metric": metric_name,
        "window": {"start": start_dt.isoformat(), "end": end_dt.isoformat()},
        "safety": {"unsafe": list(set(unsafe)), "suspicious": list(set(suspicious))},
    }


def _parse_relative_times(
    start_expr: str, end_expr: str
) -> (datetime.datetime, datetime.datetime):
    """
    Token parser reused from earlier modules.
    """
    now = datetime.datetime.utcnow()
    if start_expr.startswith("-"):
        amount, unit = (
            start_expr[1:].split("m")
            if start_expr.endswith("m")
            else start_expr[1:].split("h")
        )
        amount = int(amount)
        dt = now - (
            datetime.timedelta(minutes=amount)
            if unit.endswith("m")
            else datetime.timedelta(hours=amount)
        )
    else:
        dt = datetime.datetime.fromisoformat(start_expr.replace("Z", "+00:00"))
    start_dt = dt

    if end_expr.startswith("-"):
        amount, unit = (
            end_expr[1:].split("m")
            if end_expr.endswith("m")
            else end_expr[1:].split("h")
        )
        amount = int(amount)
        dt = now - (
            datetime.timedelta(minutes=amount)
            if unit.endswith("m")
            else datetime.timedelta(hours=amount)
        )
    else:
        dt = datetime.datetime.fromisoformat(end_expr.replace("Z", "+00:00"))
    end_dt = dt
    return start_dt, end_dt


# Example usage (feel free to delete or move to a test module)
if __name__ == "__main__":
    safety_report = check_annotation_safety(
        provider="Datadog",
        metric_name="system.cpu.user",
        start_relative="now-30m",
        end_relative="now",
    )
    print("Safety report:", safety_report)
