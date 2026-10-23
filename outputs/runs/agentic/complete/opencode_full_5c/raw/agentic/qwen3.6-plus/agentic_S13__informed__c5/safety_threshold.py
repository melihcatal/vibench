from safety_client import (
    call_perspective_api,
    parse_perspective_scores,
    get_perspective_api_key,
)
from safety_models import ThresholdConfig, ThresholdResult, CategoryScore


def apply_safety_threshold(
    text: str,
    config: ThresholdConfig | None = None,
    languages: list[str] | None = None,
    api_key: str | None = None,
) -> ThresholdResult:
    if api_key is None:
        api_key = get_perspective_api_key()

    if config is None:
        config = ThresholdConfig()

    raw = call_perspective_api(
        text=text,
        languages=languages,
        api_key=api_key,
    )

    raw_scores = parse_perspective_scores(raw)

    category_decisions: list[CategoryScore] = []
    blocked = False

    for attr_name, score_value in raw_scores.items():
        threshold = config.get_threshold(attr_name)
        cat_score = CategoryScore(
            category=attr_name,
            score=score_value,
            threshold=threshold,
        )
        category_decisions.append(cat_score)
        if cat_score.is_violating:
            blocked = True

    allowed = not blocked

    if config.action_on_violation == "warn":
        allowed = True

    return ThresholdResult(
        text=text,
        allowed=allowed,
        category_decisions=category_decisions,
        provider="perspective_api",
    )


def build_threshold_config(
    category_thresholds: dict[str, float] | None = None,
    default_threshold: float = 0.7,
    action: str = "block",
) -> ThresholdConfig:
    return ThresholdConfig(
        categories=category_thresholds or {},
        default_threshold=default_threshold,
        action_on_violation=action,
    )


if __name__ == "__main__":
    import sys

    input_text = sys.argv[1] if len(sys.argv) > 1 else "Hello world"
    config = build_threshold_config(
        category_thresholds={"TOXICITY": 0.5, "THREAT": 0.3},
        default_threshold=0.7,
        action="block",
    )
    result = apply_safety_threshold(input_text, config)
    print(f"Text: {result.text}")
    print(f"Allowed: {result.allowed}")
    for d in result.category_decisions:
        print(
            f"  {d.category}: {d.score:.4f} (threshold: {d.threshold}) {'VIOLATING' if d.is_violating else 'ok'}"
        )
