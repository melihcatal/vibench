from __future__ import annotations

from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import (
    build_moderation_request,
    category_severity_map,
    get_content_safety_client,
)
from safety_models import ModerationResult, build_score


def moderate_text(text: str, language: str = "en") -> ModerationResult:
    request = build_moderation_request(text=text, language=language)
    client = get_content_safety_client()
    response = client.analyze_text(AnalyzeTextOptions(text=request.text))
    severities = category_severity_map(response)
    scores = [
        build_score(category=category, severity=severity)
        for category, severity in severities.items()
    ]
    flagged = any(score.severity >= 4 for score in scores)
    reasons = [score.category for score in scores if score.severity >= 4]
    return ModerationResult(
        text=request.text,
        action="block" if flagged else "allow",
        flagged=flagged,
        provider="Azure AI Content Safety",
        scores=scores,
        reasons=reasons,
        raw_response={"categories": severities},
    )
