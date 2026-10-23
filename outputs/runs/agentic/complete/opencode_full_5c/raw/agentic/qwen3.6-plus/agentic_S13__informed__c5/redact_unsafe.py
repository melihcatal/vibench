from safety_client import (
    call_perspective_api,
    parse_perspective_scores,
    parse_perspective_spans,
    get_perspective_api_key,
)
from safety_models import ModerationRequest, UnsafeSpan, RedactionResult

DEFAULT_REDACTION_THRESHOLDS = {
    "TOXICITY": 0.7,
    "SEVERE_TOXICITY": 0.5,
    "IDENTITY_ATTACK": 0.6,
    "INSULT": 0.6,
    "PROFANITY": 0.7,
    "THREAT": 0.4,
    "SEXUALLY_EXPLICIT": 0.6,
    "FLIRTATION": 0.7,
}

REDACTION_MARKER = "[REDACTED]"


def redact_unsafe(
    text: str,
    thresholds: dict[str, float] | None = None,
    redaction_marker: str = REDACTION_MARKER,
    languages: list[str] | None = None,
    api_key: str | None = None,
) -> RedactionResult:
    if api_key is None:
        api_key = get_perspective_api_key()

    if thresholds is None:
        thresholds = DEFAULT_REDACTION_THRESHOLDS

    raw = call_perspective_api(
        text=text,
        languages=languages,
        api_key=api_key,
    )

    raw_scores = parse_perspective_scores(raw)
    spans_by_category = parse_perspective_spans(raw)

    unsafe_spans: list[UnsafeSpan] = []

    for category, spans in spans_by_category.items():
        threshold = thresholds.get(category, 0.7)
        score = raw_scores.get(category, 0.0)

        if score >= threshold:
            for span_info in spans:
                unsafe_spans.append(
                    UnsafeSpan(
                        text=text[span_info["begin"] : span_info["end"]],
                        start=span_info["begin"],
                        end=span_info["end"],
                        category=category,
                        score=score,
                    )
                )

    if not unsafe_spans:
        return RedactionResult(
            original_text=text,
            redacted_text=text,
            unsafe_spans=[],
            provider="perspective_api",
        )

    unsafe_spans.sort(key=lambda s: s.start)

    merged_spans: list[UnsafeSpan] = []
    for span in unsafe_spans:
        if merged_spans and span.start <= merged_spans[-1].end:
            prev = merged_spans[-1]
            if span.end > prev.end:
                merged_spans[-1] = UnsafeSpan(
                    text=text[prev.start : span.end],
                    start=prev.start,
                    end=span.end,
                    category=prev.category,
                    score=max(prev.score, span.score),
                )
        else:
            merged_spans.append(span)

    parts = []
    last_end = 0
    for span in merged_spans:
        parts.append(text[last_end : span.start])
        parts.append(redaction_marker)
        last_end = span.end
    parts.append(text[last_end:])

    redacted_text = "".join(parts)

    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        unsafe_spans=merged_spans,
        provider="perspective_api",
    )


if __name__ == "__main__":
    import sys

    input_text = sys.argv[1] if len(sys.argv) > 1 else "Hello world"
    result = redact_unsafe(input_text)
    print(f"Original: {result.original_text}")
    print(f"Redacted: {result.redacted_text}")
    print(f"Unsafe spans: {len(result.unsafe_spans)}")
    for s in result.unsafe_spans:
        print(f"  [{s.category}] '{s.text}' at {s.start}:{s.end} score={s.score:.4f}")
