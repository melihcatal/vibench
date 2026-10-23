from typing import Optional, List
from openai import OpenAI
from openai.types import ModerationCreateResponse
from model_client import create_openai_client
from model_models import SafetyCheckResult, SafetyViolation


SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]

SEVERITY_THRESHOLDS = {
    "low": 0.3,
    "medium": 0.5,
    "high": 0.75,
    "critical": 0.9,
}


def check_platform_output_safety(
    text: str,
    client: Optional[OpenAI] = None,
    threshold: float = 0.5,
) -> SafetyCheckResult:
    if client is None:
        client = create_openai_client()
    response: ModerationCreateResponse = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    violations: List[SafetyViolation] = []
    overall_flagged = result.flagged
    for category in SAFETY_CATEGORIES:
        category_scores = getattr(
            result.category_scores, category.replace("/", "_").replace("-", "_"), None
        )
        category_flagged = getattr(
            result.categories, category.replace("/", "_").replace("-", "_"), None
        )
        if category_scores is not None:
            score = float(category_scores)
            is_flagged = (
                bool(category_flagged)
                if category_flagged is not None
                else score >= threshold
            )
            if score >= SEVERITY_THRESHOLDS["low"]:
                if score >= SEVERITY_THRESHOLDS["critical"]:
                    severity = "critical"
                elif score >= SEVERITY_THRESHOLDS["high"]:
                    severity = "high"
                elif score >= SEVERITY_THRESHOLDS["medium"]:
                    severity = "medium"
                else:
                    severity = "low"
                violations.append(
                    SafetyViolation(
                        category=category,
                        severity=severity,
                        score=score,
                        flagged=is_flagged,
                    )
                )
    return SafetyCheckResult(
        flagged=overall_flagged,
        violations=violations,
        request_id=response.id,
        raw_response=response,
    )


def check_safety_with_categories(
    text: str,
    categories: Optional[List[str]] = None,
    client: Optional[OpenAI] = None,
    threshold: float = 0.5,
) -> SafetyCheckResult:
    if client is None:
        client = create_openai_client()
    response: ModerationCreateResponse = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    violations: List[SafetyViolation] = []
    overall_flagged = result.flagged
    check_categories = categories if categories else SAFETY_CATEGORIES
    for category in check_categories:
        attr_name = category.replace("/", "_").replace("-", "_")
        category_scores = getattr(result.category_scores, attr_name, None)
        category_flagged = getattr(result.categories, attr_name, None)
        if category_scores is not None:
            score = float(category_scores)
            is_flagged = (
                bool(category_flagged)
                if category_flagged is not None
                else score >= threshold
            )
            if score >= SEVERITY_THRESHOLDS["low"]:
                if score >= SEVERITY_THRESHOLDS["critical"]:
                    severity = "critical"
                elif score >= SEVERITY_THRESHOLDS["high"]:
                    severity = "high"
                elif score >= SEVERITY_THRESHOLDS["medium"]:
                    severity = "medium"
                else:
                    severity = "low"
                violations.append(
                    SafetyViolation(
                        category=category,
                        severity=severity,
                        score=score,
                        flagged=is_flagged,
                    )
                )
    return SafetyCheckResult(
        flagged=overall_flagged,
        violations=violations,
        request_id=response.id,
        raw_response=response,
    )


def is_output_safe(
    text: str,
    client: Optional[OpenAI] = None,
    threshold: float = 0.5,
) -> bool:
    result = check_platform_output_safety(text, client=client, threshold=threshold)
    return not result.flagged


def get_highest_severity(
    safety_result: SafetyCheckResult,
) -> Optional[str]:
    if not safety_result.violations:
        return None
    severity_order = ["critical", "high", "medium", "low"]
    for severity in severity_order:
        for violation in safety_result.violations:
            if violation.severity == severity:
                return severity
    return None
