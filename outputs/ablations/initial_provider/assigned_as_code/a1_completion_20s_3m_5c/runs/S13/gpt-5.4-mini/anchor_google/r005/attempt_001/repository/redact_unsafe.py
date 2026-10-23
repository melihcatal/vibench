from safety_client import build_common_request, perspective_post
from safety_models import normalize_text


def redact_unsafe(payload, config=None):
    text = normalize_text(payload.get("text"))
    response = perspective_post(
        build_common_request(
            text,
            {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        ),
        config=config,
    )
    spans = []
    for key in ("TOXICITY", "INSULT", "THREAT"):
        span_scores = response.get("attributeScores", {}).get(key, {}).get("spanScores", [])
        for span in span_scores:
            begin = span.get("begin", 0)
            end = span.get("end", 0)
            spans.append({"category": key, "begin": begin, "end": end})
    redacted = text
    for span in sorted(spans, key=lambda item: (item["begin"], item["end"]), reverse=True):
        redacted = redacted[:span["begin"]] + "[REDACTED]" + redacted[span["end"]:]
    return {"text": text, "redacted_text": redacted, "spans": spans}
