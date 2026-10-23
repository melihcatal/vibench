from typing import Optional

from safety_models import (
    ModerationRequest,
    ModerationResponse,
    ThresholdConfig,
    ModerationDecision,
    SafetyCategory,
    load_threshold_config,
    normalize_category_scores,
    determine_decision,
    response_to_dict,
)
from safety_client import (
    moderate_single,
    get_client,
    build_analyze_options,
    parse_azure_response,
)


def apply_thresholds(
    text: str,
    thresholds: Optional[ThresholdConfig] = None,
    user_id: Optional[str] = None,
) -> dict:
    if thresholds is None:
        thresholds = load_threshold_config()

    request = ModerationRequest(text=text, user_id=user_id)
    response = moderate_single(request)

    adjusted_scores = []
    for cs in response.category_scores:
        flag_thresh = thresholds.get_threshold(cs.category, "flag")
        block_thresh = thresholds.get_threshold(cs.category, "block")
        adjusted_scores.append(
            {
                "category": cs.category.value,
                "score": cs.score,
                "flag_threshold": flag_thresh,
                "block_threshold": block_thresh,
                "exceeds_flag": cs.score >= flag_thresh,
                "exceeds_block": cs.score >= block_thresh,
                "severity": cs.severity,
            }
        )

    decision, flagged = determine_decision(response.category_scores, thresholds)

    return {
        "text": text,
        "user_id": user_id,
        "decision": decision.value,
        "flagged_categories": [c.value for c in flagged],
        "threshold_config": {
            "flag_threshold": thresholds.flag_threshold,
            "block_threshold": thresholds.block_threshold,
            "category_overrides": {
                k.value: v for k, v in thresholds.category_overrides.items()
            },
        },
        "category_analysis": adjusted_scores,
        "raw_scores": response.raw_scores,
        "metadata": response.metadata,
    }


def check_threshold_compliance(
    text: str,
    custom_thresholds: dict[str, float],
    user_id: Optional[str] = None,
) -> dict:
    overrides = {}
    for cat_name, thresh in custom_thresholds.items():
        try:
            overrides[SafetyCategory(cat_name)] = thresh
        except ValueError:
            continue

    thresholds = ThresholdConfig(
        flag_threshold=0.5,
        block_threshold=0.8,
        category_overrides=overrides,
    )

    return apply_thresholds(text, thresholds=thresholds, user_id=user_id)


def get_recommended_thresholds(category: str) -> dict:
    recommendations = {
        SafetyCategory.HATE.value: {"flag": 0.4, "block": 0.7},
        SafetyCategory.SELF_HARM.value: {"flag": 0.3, "block": 0.6},
        SafetyCategory.SEXUAL.value: {"flag": 0.5, "block": 0.8},
        SafetyCategory.VIOLENCE.value: {"flag": 0.4, "block": 0.75},
        SafetyCategory.HARASSMENT.value: {"flag": 0.45, "block": 0.7},
    }
    return recommendations.get(category, {"flag": 0.5, "block": 0.8})
