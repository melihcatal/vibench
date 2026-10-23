from safety_client import (
    get_openai_client,
    validate_text_input,
    OPENAI_MODERATION_MODEL,
)
from safety_models import ModerationResult, ThresholdConfig


def apply_thresholds(text, thresholds=None, message_id=None):
    validated = validate_text_input(text)
    if thresholds is None:
        thresholds = ThresholdConfig()
    client = get_openai_client()
    response = client.moderations.create(
        input=validated,
        model=OPENAI_MODERATION_MODEL,
    )
    result = response.results[0]
    moderation_result = ModerationResult.from_openai_response(
        text=validated,
        result=result,
        message_id=message_id,
    )
    threshold_dict = thresholds.to_dict()
    score_dict = moderation_result.category_scores.to_dict()
    exceeded = {}
    for category, threshold_val in threshold_dict.items():
        score_val = score_dict.get(category, 0.0)
        if score_val >= threshold_val:
            exceeded[category] = {
                "score": score_val,
                "threshold": threshold_val,
                "exceeded_by": score_val - threshold_val,
            }
    threshold_flagged = len(exceeded) > 0
    return {
        "moderation_result": moderation_result,
        "threshold_flagged": threshold_flagged,
        "exceeded_categories": exceeded,
        "thresholds_applied": threshold_dict,
        "decision": "block" if threshold_flagged else "allow",
    }


def apply_thresholds_batch(texts, thresholds=None, message_ids=None):
    if thresholds is None:
        thresholds = ThresholdConfig()
    results = []
    for i, text in enumerate(texts):
        mid = message_ids[i] if message_ids and i < len(message_ids) else None
        results.append(apply_thresholds(text, thresholds, mid))
    return results


def apply_strict_thresholds(text, message_id=None):
    return apply_thresholds(text, ThresholdConfig.strict(), message_id)


def apply_permissive_thresholds(text, message_id=None):
    return apply_thresholds(text, ThresholdConfig.permissive(), message_id)


def get_threshold_recommendation(result):
    if result["threshold_flagged"]:
        exceeded = result["exceeded_categories"]
        critical = [
            k
            for k in exceeded
            if k
            in (
                "self_harm",
                "self_harm_intent",
                "self_harm_instructions",
                "sexual_minors",
            )
        ]
        if critical:
            return {
                "action": "immediate_block",
                "reason": "Critical safety categories exceeded",
                "categories": critical,
            }
        return {
            "action": "block_and_review",
            "reason": "Policy-violating categories exceeded thresholds",
            "categories": list(exceeded.keys()),
        }
    return {
        "action": "allow",
        "reason": "All category scores within acceptable thresholds",
        "categories": [],
    }
