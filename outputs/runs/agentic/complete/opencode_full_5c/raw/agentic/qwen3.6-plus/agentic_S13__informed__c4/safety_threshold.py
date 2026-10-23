from azure.ai.contentsafety import ContentSafetyClient
from safety_client import (
    get_content_safety_client,
    build_analyze_text_payload,
    parse_analyze_text_response,
)
from safety_models import ThresholdResult


DEFAULT_THRESHOLDS: dict[str, int] = {
    "Hate": 2,
    "SelfHarm": 1,
    "Sexual": 2,
    "Violence": 2,
}


def safety_threshold(
    text: str,
    thresholds: dict[str, int] | None = None,
    categories: list[str] | None = None,
    client: ContentSafetyClient | None = None,
) -> ThresholdResult:
    if client is None:
        client = get_content_safety_client()
    effective_thresholds = thresholds or DEFAULT_THRESHOLDS
    payload = build_analyze_text_payload(text=text, categories=categories)
    response = client.analyze_text(payload)
    parsed = parse_analyze_text_response(response)
    category_decisions: dict[str, dict[str, str | int | bool]] = {}
    any_blocked = False
    blocking_reasons = []
    for cat_name, cat_info in parsed["categories"].items():
        threshold = effective_thresholds.get(cat_name, 1)
        severity_value = cat_info["severity_value"]
        allowed = severity_value < threshold
        if not allowed:
            any_blocked = True
            blocking_reasons.append(
                f"{cat_name} severity {cat_info['severity']} ({severity_value}) exceeds threshold {threshold}"
            )
        category_decisions[cat_name] = {
            "severity": cat_info["severity"],
            "severity_value": severity_value,
            "threshold": threshold,
            "allowed": allowed,
        }
    if any_blocked:
        reason = "Blocked: " + "; ".join(blocking_reasons)
    else:
        reason = "All categories within thresholds"
    return ThresholdResult(
        text=text,
        allowed=not any_blocked,
        category_decisions=category_decisions,
        reason=reason,
    )
