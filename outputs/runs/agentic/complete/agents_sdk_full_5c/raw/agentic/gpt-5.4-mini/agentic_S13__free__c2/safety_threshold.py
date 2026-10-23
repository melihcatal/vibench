from openai import OpenAI

from safety_client import get_client, load_config
from safety_models import ModerationDecision, ThresholdPolicy, normalize_text


def apply_thresholds(text: str, policy: ThresholdPolicy) -> ModerationDecision:
    cfg = load_config()
    client: OpenAI = get_client(cfg)
    normalized = normalize_text(text)
    result = client.moderations.create(model="omni-moderation-latest", input=normalized)
    item = result.results[0]
    allowed = True
    for category, threshold in policy.thresholds.items():
        score = float(item.category_scores.get(category, 0.0))
        if score >= threshold:
            allowed = False
            break
    return ModerationDecision(
        allowed=allowed and not item.flagged,
        categories=dict(item.categories),
        scores=dict(item.category_scores),
        model="omni-moderation-latest",
        raw=result.model_dump() if hasattr(result, "model_dump") else None,
    )
