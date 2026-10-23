from safety_client import (
    call_perspective_api,
    parse_perspective_scores,
    get_perspective_api_key,
    PERSPECTIVE_API_BASE_URL,
)
from safety_models import ModerationRequest, ModerationResponse, CategoryScore

DEFAULT_THRESHOLDS = {
    "TOXICITY": 0.7,
    "SEVERE_TOXICITY": 0.5,
    "IDENTITY_ATTACK": 0.6,
    "INSULT": 0.6,
    "PROFANITY": 0.7,
    "THREAT": 0.4,
    "SEXUALLY_EXPLICIT": 0.6,
    "FLIRTATION": 0.7,
}


def moderate_text(
    text: str,
    languages: list[str] | None = None,
    thresholds: dict[str, float] | None = None,
    api_key: str | None = None,
) -> ModerationResponse:
    if api_key is None:
        api_key = get_perspective_api_key()

    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    raw = call_perspective_api(
        text=text,
        languages=languages,
        api_key=api_key,
    )

    raw_scores = parse_perspective_scores(raw)

    category_scores = []
    overall_violation = False

    for attr_name, score_value in raw_scores.items():
        threshold = thresholds.get(attr_name, 0.7)
        cat_score = CategoryScore(
            category=attr_name,
            score=score_value,
            threshold=threshold,
        )
        category_scores.append(cat_score)
        if cat_score.is_violating:
            overall_violation = True

    return ModerationResponse(
        text=text,
        scores=category_scores,
        overall_violation=overall_violation,
        provider="perspective_api",
        raw_response=raw,
    )


if __name__ == "__main__":
    import sys

    input_text = sys.argv[1] if len(sys.argv) > 1 else "Hello world"
    result = moderate_text(input_text)
    print(f"Text: {result.text}")
    print(f"Overall violation: {result.overall_violation}")
    for s in result.scores:
        print(
            f"  {s.category}: {s.score:.4f} (threshold: {s.threshold}) {'VIOLATING' if s.is_violating else 'ok'}"
        )
