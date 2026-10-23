from typing import Dict, Union
from safety_client import WatsonXGuardrailsClient
from safety_models import ModerationResult


def moderate_text(text: str) -> ModerationResult:
    """Moderate text for unsafe or policy-violating content using WatsonX Guardrails."""
    client = WatsonXGuardrailsClient()
    result = client.moderate_text(text)

    return ModerationResult(
        is_safe=result["is_safe"],
        score=result["score"],
        categories=result["categories"],
        flagged_reason="HAP detection" if not result["is_safe"] else "",
    )
