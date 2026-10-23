import os
from openai import OpenAI
from speech_client import get_openai_client
from speech_models import SafetyCheckRequest, SafetyCheckResult

def check_script_safety(request: SafetyCheckRequest) -> SafetyCheckResult:
    client = get_openai_client()

    try:
        response = client.moderations.create(input=request.text)
        
        moderation_output = response.results[0]

        is_flagged = moderation_output.flagged
        categories = {cat.category: cat.flagged for cat in moderation_output.categories}
        
        return SafetyCheckResult(
            is_safe=not is_flagged,
            moderation_categories=categories
        )

    except Exception as e:
        raise RuntimeError(f"OpenAI Moderation API request failed: {e}")
