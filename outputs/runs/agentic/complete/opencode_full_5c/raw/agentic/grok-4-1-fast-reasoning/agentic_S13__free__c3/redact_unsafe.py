import requests
from safety_client import get_api_key
from safety_models import ModerationResult, Span, CategoryScore

ENDPOINT = "https://westus2.api.cognitive.microsoft.com/contentmoderator"


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> ModerationResult:
    key = get_api_key("azure_content_moderator")
    url = f"{ENDPOINT}/moderate/v1.0/ProcessText/Screen"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "text/plain; charset=utf-8",
    }
    params = {"language": "eng"}
    response = requests.post(url, headers=headers, params=params, data=text)
    response.raise_for_status()
    data = response.json()
    spans = []
    if data.get("Terms"):
        for term in data["Terms"]:
            span_text = term["Text"]
            start = term["Index"]
            end = start + len(span_text)
            spans.append(
                Span(start=start, end=end, category="profanity", text=span_text)
            )
    redacted = text
    for span in sorted(spans, key=lambda s: s.start, reverse=True):
        redacted = redacted[: span.start] + replacement + redacted[span.end :]
    prob = 1.0 if spans else 0.0
    scores = [CategoryScore(category="profanity", probability=prob)]
    flagged = bool(spans)
    result = ModerationResult(
        input_text=text, scores=scores, flagged=flagged, spans=spans
    )
    result.redacted_text = redacted
    return result
